import logging
from functools import wraps

from django.core.cache import caches

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import JSONRenderer, AdminRenderer, BrowsableAPIRenderer


class CustomRendererView:
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @property
    def renderer_classes(self):
        renderers = super().renderer_classes

        if not self.request.user.is_staff:
            renderers = [JSONRenderer,]

        return renderers

def cached(cache):
    def true_decorator(f):
        @wraps(f)
        def w(*args, **kwargs):
            instance = args[1]
            cache_key = f'{instance.facility}.{instance.id}'
            logger = logging.getLogger(__name__)
            logger.debug(f'{cache} cache_key: {cache_key}')
            try:
                data = caches[cache].get(cache_key)
                if data is not None:
                    return data
            except:
                pass
            logger.info('did not cache')
            data = f(*args, **kwargs)
            try:
                caches[cache].set(cache_key, data)
            except:
                pass
            return data
        return w
    return true_decorator