import os
import re
import datetime
import logging
import rapidjson
import secrets
import string
import time
from functools import wraps
from json import JSONEncoder
from pprint import pformat
from traceback import print_exc
from typing import Optional
from zipfile import ZipFile

from cacheops import cached
from dateutil.parser import parse as parse_date
from django.conf.global_settings import SESSION_COOKIE_DOMAIN, SESSION_COOKIE_SECURE
from django.db import transaction
from django.db.models import Model, QuerySet
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token

from django.conf import settings
from rest_framework_rapidjson.renderers import RapidJSONRenderer
from sentry_sdk import capture_exception

from e_logs.core.utils.errors import SemanticError, AccessError
from e_logs.core.utils.loggers import err_logger


def logged(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('CALL')
        logger.debug(
            f'Call {func.__name__} in {func.__module__}, line {func.__code__.co_firstlineno}\n'
            f'With arguments {args} {kwargs}')
        func_res = func(*args, **kwargs)
        logger.debug(
            f'Exiting {func.__name__} in {func.__module__}, line {func.__code__.co_firstlineno}')
        return func_res

    return wrapper


def has_private_journals(func):
    @wraps(func)
    def wrapper(self, request, plant_name, journal_name):
        if (journal_name == "report_income_outcome_schieht" or journal_name == "metals_compute") \
                and not (request.user.is_superuser or request.user.groups.filter(name='Big boss')
                .exists() or request.user.employee.name == "makagonov-s-n"):
            return HttpResponse("<h2>403</h2> <h3>нет доступа</h3>")
        return func(self, request, plant_name, journal_name)

    return wrapper


class StrJSONEncoder(JSONEncoder):
    def default(self, o):
        return str(o)


def handle_exceptions(view):
    @wraps(view)
    def wrapper(request, **kwargs):
        try:
            response = view(request, **kwargs)
        except SemanticError as e:
            response = HttpResponse(str(e))
            err_logger.error('Processed SemanticError')
            capture_exception(e)
        except AccessError as e:
            response = HttpResponse(str(e))
            err_logger.error('Processed AccessError')
            capture_exception(e)
        except Exception as e:
            err_logger.error(e)
            print_exc()
            response = {"error": "fatal"}
            capture_exception(e)

        return response

    return wrapper


def handle_response_types(view):
    @wraps(view)
    def wrapper(request, **kwargs):
        response = view(request, **kwargs)

        if not isinstance(response, (HttpResponse, JsonResponse)):
            if isinstance(response, dict):
                response["__t"] = time.time()
            if type(response) is dict:
                response = JsonResponse(response, encoder=StrJSONEncoder,
                                        json_dumps_params={'indent': 4})
            else:
                response = JsonResponse(response, safe=False, encoder=StrJSONEncoder,
                                        json_dumps_params={'indent': 4})

        return response

    return wrapper


def handle_response_headers(view):
    @wraps(view)
    def wrapper(request, **kwargs):
        response = view(request, **kwargs)

        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Credentials"] = "true"

        return response

    return wrapper


def check_auth(view):
    @wraps(view)
    def wrapper(request, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(str(SemanticError(message='Доступ запрещен. Войдите в систему.')))
        if request.method == 'POST':
            received_token = request.POST.get('token', None)
        else:
            received_token = request.GET.get('token', None)
        if received_token != request.user.employee.csrf:
            return HttpResponse(str(SemanticError(message='Сессия истекла. Обновите страницу.')))

        response = view(request, **kwargs)
        return response

    return wrapper


def process_json_view(auth_required=True):
    """
    This is view function annotation. It'll try to handle error, encode things in json, set all required headers
    and check auth and CSRF if required.
    :param auth_required:
    :return:
    """

    def real_decorator(view):
        @logged
        @csrf_exempt
        @handle_response_headers
        @handle_response_types
        @handle_exceptions
        @transaction.atomic
        def wrapper(request, **kwargs):
            # TODO: use @login_required?
            if auth_required:
                return check_auth(view(request, **kwargs))
            else:
                return view(request, **kwargs)

        return wrapper

    return real_decorator


def generate_csrf() -> str:
    return ''.join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(settings.CSRF_LENGTH))


def parse(s: str) -> timezone.datetime:
    return timezone.make_aware(parse_date(s))


def max_cache(func):
    return cached(timeout=settings.MAX_CACHE_TIME)(func)


def model_to_dict(model: Model) -> dict:
    return {f.name: getattr(model, f.name) for f in model._meta.get_fields(include_parents=False)}


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def set_cookie(response, key: str, value: str, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() +
                                         datetime.timedelta(seconds=max_age),
                                         "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires,
                        domain=SESSION_COOKIE_DOMAIN,
                        secure=SESSION_COOKIE_SECURE or None)


def default_if_error(value):
    def real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                capture_exception(e)
                return value

        return wrapper

    return real_decorator


def none_if_error(func):
    return default_if_error(None)(func)


def filter_or_none(model, *args, **kwargs) -> Optional[QuerySet]:
    try:
        return model.objects.filter(*args, **kwargs)
    except model.DoesNotExist:
        return None


def get_or_none(model, *args, **kwargs) -> Optional[QuerySet]:
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def model_to_representation(model: Model):
    def is_printable(field):
        excluded_types = ['ManyToManyField', 'ForeignKey']
        if not hasattr(field, 'get_internal_type'):
            return False
        if field.get_internal_type() in excluded_types:
            return False
        return True

    def name_or_none(model, field):
        try:
            # return field.name, field.get_internal_type()
            return getattr(model, field.name)
        except:
            return None

    return {f.name: name_or_none(model, f) for f in
            model._meta.get_fields(include_parents=False)
            if is_printable(f)}

def current_date():
    return timezone.get_current_timezone().normalize(timezone.now()).date()

class StrAsDictMixin:
    # def __str__(self: Model):
    #     return str(self.__class__.__name__) + format(model_to_representation(self))
    pass


def zipdir(basedir, archivename):
    assert os.path.isdir(basedir)
    with ZipFile(archivename, "w") as z:
        for root, dirs, files in os.walk(basedir):
            #NOTE: ignore empty directories
            for fn in files:
                absfn = os.path.join(root, fn)
                zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
                z.write(absfn, zfn)
