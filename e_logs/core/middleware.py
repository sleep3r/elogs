import re
import traceback
import logging

from channels.auth import AuthMiddlewareStack
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError
from rest_framework.authtoken.models import Token

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