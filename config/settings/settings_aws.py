from .settings_base import *



ALLOWED_HOSTS = ['*']

CHANNEL_LAYERS = {
     "default": {
         "BACKEND": "channels_redis.core.RedisChannelLayer",
         "CONFIG": {
            "hosts": [("redis", 6379)],
         },
     },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379?db=0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.lz4.Lz4Compressor",
            "IGNORE_EXCEPTIONS": True,
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
        },
        'TIMEOUT': MAX_CACHE_TIME,
        "KEY_PREFIX": '',
    }
}

CACHEOPS_REDIS = {
    'host': 'redis',
    'port': 6379,
    'db': 1,
}

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'DjangoRelease',
        'HOST': '88.99.2.149',
        'PORT': '',
        'USER': 'InframineDeveloper',
        'PASSWORD': 'Singapore2017',

        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'elogs',
        'HOST': 'db',
        'PORT': '1433',
        'USER': 'sa',
        'PASSWORD': 'Singapore2017',

        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
}


DEBUG = False

TEMPLATES[0]['OPTIONS']['loaders'] = [  # noqa F405
    (
        'django.template.loaders.cached.Loader',
        [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
    ),
]

TEMPLATES[0]['APP_DIRS'] = False


MIDDLEWARE.insert(1, 'django.middleware.gzip.GZipMiddleware')
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

MIDDLEWARE = [] + MIDDLEWARE + \
             [
                 'htmlmin.middleware.HtmlMinifyMiddleware',
                 'htmlmin.middleware.MarkRequestMiddleware',
             ]
HTML_MINIFY = True
