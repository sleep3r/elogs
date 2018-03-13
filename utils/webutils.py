import json
import secrets
import string
import time
from collections import defaultdict
from traceback import print_exc

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dateutil.parser import parse as parse_date
from django.utils import timezone

from utils.errors import SemanticError, AccessError

# view accepts HttpRequest
# view returns dict or defaultdict
from utils.settings import webURL, CSRF_LENGTH


def processView(auth_required=True):
    def real_decorator(view):
        def w(request, **kwargs):
            if auth_required:
                if not request.user.is_authenticated():
                    return HttpResponse(str(SemanticError(message='Доступ запрещен. Войдите в систему.')))
                if request.method == 'POST':
                    received_token = request.POST.get('token', None)
                else:
                    received_token = request.GET.get('token', None)
                if received_token != request.user.employee.csrf:
                    return HttpResponse(str(SemanticError(message='Сессия истекла. Обновите страницу.')))
            try:
                response = view(request, **kwargs)
            except SemanticError as e:
                response = HttpResponse(str(e))
            except AccessError as e:
                response = HttpResponse(str(e))
            except Exception as e:
                print(e)
                print_exc()
                response = {"error": "fatal"}

            if type(response) is not HttpResponse:
                if type(response) in (dict, defaultdict):
                    response["__t"] = time.time()
                if type(response) is not str:
                    response = json.dumps(response)
                response = HttpResponse(response)

            response["Access-Control-Allow-Origin"] = webURL
            response["Access-Control-Allow-Methods"] = "POST, POST, OPTIONS"
            response["Access-Control-Allow-Credentials"] = "true"
            return response

        return csrf_exempt(w)
    return real_decorator


def generate_csrf():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(CSRF_LENGTH))


def parse(s):
    return timezone.make_aware(parse_date(s))