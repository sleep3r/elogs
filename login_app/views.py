import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import views, authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from utils.webutils import processView, generate_csrf


def build_auth_object(user):
    if user is None or not user.is_active or user.is_anonymous():
        return dict()
    user.employee.csrf = generate_csrf()
    user.employee.save()
    return {
        'user': user.id,
        'name': user.first_name + ' ' + user.last_name,
        'department': user.employee.department.name,
        'token': user.employee.csrf
    }


@processView(auth_required=True)
def change_password(request):
    pwd = request.POST['pwd']
    chpwd = request.POST['chpwd']
    u = request.user
    if u.check_password(pwd) and len(chpwd) > 3:
        u.set_password(chpwd)
        u.save()
        user = authenticate(username=u.username, password=chpwd)
        if user is not None and user.is_active:
            login(request, user)
        res = {'ok': 1, 'username': u.username}
    else:
        res = {'ok': 0, 'username': u.username}
    return HttpResponse(json.dumps(res))


@processView(auth_required=False)
def login_auth(request):
    username = request.POST['username']
    password = request.POST['pwd']
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        response = build_auth_object(user)
    else:
        response = dict()

    return response


@processView(auth_required=True)
def logout_view(request):
    logout(request)
    return HttpResponse('{}')


@processView(auth_required=False)
def get_user(request):
    return build_auth_object(request.user)
