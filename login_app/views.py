import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import views, authenticate, login, logout
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from utils.webutils import process_json_view, generate_csrf


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
def logout_view(request):
    logout(request)
    return login_page(request, error=None)


def login_page(request, error=None):
    context = {'error': error, 'next': '?next=' + (request.GET.get('next') or '/')}
    template = loader.get_template('login.html')
    return HttpResponse(template.render(context, request))


