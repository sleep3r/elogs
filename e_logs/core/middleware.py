import re
import traceback
import logging

from django.conf import settings
from channels.auth import AuthMiddlewareStack
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError
from rest_framework.authtoken.models import Token
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject


logger = logging.getLogger(__name__)


class TokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope['headers'])
        auth_header = None
        try:
            auth_header = _str_to_dict(headers[b'cookie'].decode())['Authorization']
        except:
            pass

        logger.info(auth_header)

        if auth_header:
            try:
                token = Token.objects.get(key=auth_header)
                scope['user'] = token.user
            except (InvalidSignatureError, KeyError, ExpiredSignatureError, DecodeError):
                traceback.print_exc()
                pass
            except Exception as e:  # NoQA
                logger.error(scope)
                traceback.print_exc()

        return self.inner(scope)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))


def _str_to_dict(str):
    return {k: v.strip('"') for k, v in re.findall(r'(\S+)=(".*?"|\S+)', str)}

def user_from_asgi_request(request):
    auth_token = _str_to_dict(dict(request.scope['headers'])[b'cookie'].decode())['Authorization']
    return Token.objects.get(key=auth_token).user

class CustomAuthenticationMiddleware(MiddlewareMixin):
    ''' Overwritten to work with rest_framework auth '''

    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE%s setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        ) % ("_CLASSES" if settings.MIDDLEWARE is None else "")
        request.user = SimpleLazyObject(lambda: user_from_asgi_request(request))
