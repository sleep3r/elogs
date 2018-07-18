import datetime
import json
import secrets
import string
import time
from collections import defaultdict
from json import JSONEncoder
from traceback import print_exc

from django.conf.global_settings import SESSION_COOKIE_DOMAIN, SESSION_COOKIE_SECURE
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dateutil.parser import parse as parse_date
from django.utils import timezone

from utils.errors import SemanticError, AccessError

# view accepts HttpRequest
# view returns dict or defaultdict
from utils.settings import webURL, CSRF_LENGTH


class StrJSONEncoder(JSONEncoder):
    def default(self, o):
        return str(o)


def process_json_view(auth_required=True):
    """
    This is view function annotation. It'll try to handle error, encode things in json, set all required headers
    and check auth and CSRF if required.
    :param auth_required:
    :return:
    """
    def real_decorator(view):
        def w(request, **kwargs):
            if auth_required:
                if not request.user.is_authenticated:
                    return HttpResponse(str(SemanticError(message='Доступ запрещен. Войдите в систему.')))
                if request.method == 'POST':
                    received_token = request.POST.get('token', None)
                else:
                    received_token = request.GET.get('token', None)
                if received_token != request.user.employee.csrf:
                    return HttpResponse(str(SemanticError(message='Сессия истекла. Обновите страницу.')))
            try:
                with transaction.atomic():
                    response = view(request, **kwargs)
            except SemanticError as e:
                response = HttpResponse(str(e))
            except AccessError as e:
                response = HttpResponse(str(e))
            except Exception as e:
                print(e)
                print_exc()
                response = {"error": "fatal"}

            if not isinstance(response, (HttpResponse, JsonResponse)):
                if isinstance(response, dict):
                    response["__t"] = time.time()
                if type(response) is dict:
                    response = JsonResponse(response, encoder=StrJSONEncoder, json_dumps_params={'indent': 4})
                else:
                    response = JsonResponse(response, safe=False, encoder=StrJSONEncoder, json_dumps_params={'indent': 4})

            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            response["Access-Control-Allow-Credentials"] = "true"

            return response

        return csrf_exempt(w)
    return real_decorator


def generate_csrf():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(CSRF_LENGTH))


def parse(s):
    return timezone.make_aware(parse_date(s))


def translate(name):
    # Заменяем пробелы и преобразуем строку к нижнему регистру
    name = name.replace(' ', '-').lower()
    transtable = (
        ## Большие буквы
        (u"Щ", u"Sch"),
        (u"Щ", u"SCH"),
        # two-symbol
        (u"Ё", u"Yo"),
        (u"Ё", u"YO"),
        (u"Ж", u"Zh"),
        (u"Ж", u"ZH"),
        (u"Ц", u"Ts"),
        (u"Ц", u"TS"),
        (u"Ч", u"Ch"),
        (u"Ч", u"CH"),
        (u"Ш", u"Sh"),
        (u"Ш", u"SH"),
        (u"Ы", u"Yi"),
        (u"Ы", u"YI"),
        (u"Ю", u"Yu"),
        (u"Ю", u"YU"),
        (u"Я", u"Ya"),
        (u"Я", u"YA"),
        # one-symbol
        (u"А", u"A"),
        (u"Б", u"B"),
        (u"В", u"V"),
        (u"Г", u"G"),
        (u"Д", u"D"),
        (u"Е", u"E"),
        (u"З", u"Z"),
        (u"И", u"I"),
        (u"Й", u"J"),
        (u"К", u"K"),
        (u"Л", u"L"),
        (u"М", u"M"),
        (u"Н", u"N"),
        (u"О", u"O"),
        (u"П", u"P"),
        (u"Р", u"R"),
        (u"С", u"S"),
        (u"Т", u"T"),
        (u"У", u"U"),
        (u"Ф", u"F"),
        (u"Х", u"H"),
        (u"Э", u"E"),
        (u"Ъ", u"`"),
        (u"Ь", u"'"),
        ## Маленькие буквы
        # three-symbols
        (u"щ", u"sch"),
        # two-symbols
        (u"ё", u"yo"),
        (u"ж", u"zh"),
        (u"ц", u"ts"),
        (u"ч", u"ch"),
        (u"ш", u"sh"),
        (u"ы", u"yi"),
        (u"ю", u"yu"),
        (u"я", u"ya"),
        # one-symbol
        (u"а", u"a"),
        (u"б", u"b"),
        (u"в", u"v"),
        (u"г", u"g"),
        (u"д", u"d"),
        (u"е", u"e"),
        (u"з", u"z"),
        (u"и", u"i"),
        (u"й", u"j"),
        (u"к", u"k"),
        (u"л", u"l"),
        (u"м", u"m"),
        (u"н", u"n"),
        (u"о", u"o"),
        (u"п", u"p"),
        (u"р", u"r"),
        (u"с", u"s"),
        (u"т", u"t"),
        (u"у", u"u"),
        (u"ф", u"f"),
        (u"х", u"h"),
        (u"э", u"e"),
        (u"ь", ""),
    )
    # перебираем символы в таблице и заменяем
    for symb_in, symb_out in transtable:
        name = name.replace(symb_in, symb_out)
    # возвращаем переменную
    return name


def model_to_dict(model):
    return {f.name: getattr(model, f.name) for f in model._meta.get_fields(include_parents=False)}


def set_cookie(response, key, value, days_expire = 7):
  if days_expire is None:
    max_age = 365 * 24 * 60 * 60  #one year
  else:
    max_age = days_expire * 24 * 60 * 60
  expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
  response.set_cookie(key, value, max_age=max_age, expires=expires, domain=SESSION_COOKIE_DOMAIN, secure=SESSION_COOKIE_SECURE or None)