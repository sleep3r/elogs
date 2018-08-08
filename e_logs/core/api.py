import logging
from functools import wraps

from django.core.cache import cache

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

def cached(cache_key):
    def real_decorator(f):
        @wraps(f)
        def w(*args, **kwargs):
            logger = logging.getLogger(__name__)
            data_id = args[1]['id']
            try:
                data = cache.get(f'{cache_key}_{data_id}')
                if data is not None:
                    logger.info(f'get cache, cache_key: {cache_key}_{data_id}')
                    return data
                else:
                    logger.info(f'no cache, cache_key: {cache_key}_{data_id}')
                    data = f(*args, **kwargs)
                    try:
                        cache.set(f'{cache_key}_{data_id}', data)
                        return data
                    except:
                        logger.info(f'setting cache error, cache_key: {cache_key}_{data_id}')
            except:
                logger.info(f'getting cache error, cache_key: {cache_key}_{data_id}')
        return w
    return real_decorator