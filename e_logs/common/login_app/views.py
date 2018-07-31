import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import views, authenticate, login, logout
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from e_logs.common.messages_app.models import Message

from e_logs.core.utils.deep_dict import deep_dict
from e_logs.core.utils.errors import AccessError
from e_logs.core.utils.webutils import process_json_view, generate_csrf, model_to_dict, set_cookie, logged


@process_json_view(auth_required=False)
def login_auth(request):
    username = request.POST.get('username') or ''
    password = request.POST.get('password') or ''

    user = authenticate(username=username, password=password)
    if user is not None and user.is_active and user.employee is not None:
        login(request, user)
        response = redirect(request.GET.get('next') or '/')
    else:
        return login_page(request, error='Неверное имя пользователя или пароль!')

    return response


@process_json_view(auth_required=False)
@logged
def logout_view(request):
    logout(request)
    return login_page(request, error=None)


@logged
def login_page(request, error=None):
    context = {'error': error, 'next': '?next=' + (request.GET.get('next') or '/')}

    template = loader.get_template('login.html')
    response = HttpResponse(template.render(context, request))

    return response
