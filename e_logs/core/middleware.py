import re
import traceback
import logging

from django.conf import settings
from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError
from rest_framework.authtoken.models import Token
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject


logger = logging.getLogger(__name__)


def str_to_dict(str):
    return {k: v.strip('"') for k, v in re.findall(r'(\S+)=(".*?"|\S+)', str)}


class TokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope['headers'])
        auth_header = None
        try:
            auth_header = str_to_dict(headers[b'cookie'].decode())['Authorization']
        except:
            pass

        logger.info(auth_header)

        if auth_header:
            try:
                token = Token.objects.get(key=auth_header)
                scope['user'] = token.user
            except:
                scope['user'] = AnonymousUser()

        return self.inner(scope)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))


def user_from_asgi_request(request):
    headers = dict(request.scope['headers'])
    auth_token = str_to_dict(headers[b'cookie'].decode())['Authorization']
    return Token.objects.get(key=auth_token).user


class CustomAuthenticationMiddleware(MiddlewareMixin):
    """ Overwritten to work with rest_framework auth """

    def user_from_asgi_request(self, request):
        if not hasattr(request, '_cached_user'):
            print(request.__dict__)
            print(request.__dict__.keys())
            print(request.COOKIES['Authorization'])
            try:
                auth_token = request.COOKIES['Authorization']
                request._cached_user = Token.objects.get(key=auth_token).user
            except:
                try:
                    request._cached_user = request.user
                except:
                    request._cached_user = AnonymousUser()
        return request._cached_user

    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE%s setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        ) % ("_CLASSES" if settings.MIDDLEWARE is None else "")
        request.user = SimpleLazyObject(lambda: self.user_from_asgi_request(request))
