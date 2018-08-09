from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from e_logs.core.utils.webutils import process_json_view, logged


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
