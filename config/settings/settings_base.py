import os
from pathlib import Path

import dj_database_url
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(DEBUG=(bool, False))

FIXTURE_DIRS = (BASE_DIR / 'fixtures',)
STATIC_ROOT = str(BASE_DIR / 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / 'static']
LOCALE_PATHS = [BASE_DIR / 'resources/locale']
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

LOGIN_URL = '/auth/login_page'
LOGOUT_URL = '/auth/logout'
ADMIN_URL = 'admin/'
STATIC_URL = '/static/'

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.routing.application'

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', env("HOSTNAME")]
FEEDBACK_TG_BOT = {
    "token": env("TG_TOKEN"),
    "channel": env("TG_CHANNEL"),
    "channel_name": env("TG_CHANNEL_NAME"),
    "url": env("TG_PROXY_URL"),
}

DATABASE_URL = env('DATABASE_URL')
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],

            'libraries': {
                'express_tags': 'e_logs.core.templatetags.express_tags',
            }
        },
    },
]

# APPS
# ------------------------------------------------------------------------------
THIRD_PARTY_APPS = [
    'channels',
    'rest_framework',
    'rest_framework_swagger',
    'django_filters',
    'webpack_loader',
    'django_extensions',
    'cacheops',
    'django_pickling',
    'service_objects',
    'django_celery_beat',
    'django_celery_results',
    'corsheaders',
]
LOCAL_APPS = [
    'e_logs.core.apps.CoreConfig',

    'e_logs.common.login_app.apps.LoginApp',
    'e_logs.common.all_journals_app.apps.CommonAllJournalsAppConfig',
    'e_logs.common.messages_app.apps.CommonMessagesAppConfig',
    'e_logs.common.feedback_app.apps.FeedbackAppConfig',
    'e_logs.common.data_visualization_app.apps.DataVisualizationAppConfig',
    'e_logs.common.settings_app.apps.SettingsAppConfig',

    'e_logs.furnace.fractional_app.apps.FurnaceFractionalAppConfig',

    'e_logs.business_logic.modes.apps.BLModesConfig',
    'e_logs.business_logic.blank_shifts.apps.BLBlankShiftsConfig',
]
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.humanize',  # Handy template tags
    'django.contrib.admin',
    'django.contrib.staticfiles',
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# PASSWORDS
# ------------------------------------------------------------------------------
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'webpack_bundles/',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': ['.+\.hot-update.js', '.+\.map']
    }
}

CSRF_LENGTH = 32
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
ugettext = lambda s: s
LANGUAGES = (('ru', ugettext('Russian')), ('en', ugettext('English')))

APPEND_SLASH = True

MANAGERS = ADMINS = [("""inframine""", 'inframine@inframine.io')]

if DEBUG:
    import logging

    l = logging.getLogger('django.db.backends')
    l.setLevel(logging.DEBUG)
    l.addHandler(logging.StreamHandler())

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'main_formatter': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'color_formatter': {
            '()': 'e_logs.core.utils.formatters.ColorsFormatter',
            # 'format': "[%(asctime)s] %(message)s",
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'color_formatter',
        },
        'production_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/main/main.log',
            'backupCount': 7,
            'formatter': 'color_formatter',
            'filters': ['require_debug_false'],
            'when': 'midnight',
        },
        'debug_file_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/main_debug_debug/main_debug_debug.log',
            'backupCount': 7,
            'formatter': 'color_formatter',
            'filters': ['require_debug_true'],
            'when': 'midnight',
        },
        'debug_file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/main_debug_info/main_debug_info.log',
            'backupCount': 7,
            'formatter': 'color_formatter',
            'filters': ['require_debug_true'],
            'when': 'midnight',
        },
        'debug_file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/main_debug_error/main_debug_error.log',
            'backupCount': 7,
            'formatter': 'color_formatter',
            'filters': ['require_debug_true'],
            'when': 'midnight',
        },
        'debug_file_calls': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/main_debug_calls/main_debug_calls.log',
            'backupCount': 7,
            'formatter': 'color_formatter',
            'filters': ['require_debug_true'],
            'when': 'midnight',
        },
        'printed_values': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/printed_values/printed_values.log',
            'backupCount': 7,
            'formatter': 'color_formatter',
            'filters': ['require_debug_true'],
            'when': 'midnight',
        },
        'db_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/db_log/db_log.log',
            'backupCount': 7,
            'formatter': 'color_formatter',
            'filters': ['require_debug_true'],
            'when': 'midnight',
        },
        'null': {
            "class": 'logging.NullHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'debug_file_error'],
            'level': 'ERROR',
            'propagate': True,
        },
        'py.warnings': {
            'handlers': ['console', 'debug_file_debug', 'debug_file_info', 'debug_file_error'],
        },
        '': {
            'handlers': ['production_file', 'debug_file_debug',
                         'debug_file_info', 'debug_file_error'],
            'level': "DEBUG",
        },
        'django': {
            'handlers': ['console', 'debug_file_debug', 'debug_file_info', 'debug_file_error'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db': {
            'handlers': ['db_log'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['debug_file_debug', 'console'],
            'level': 'DEBUG',
        },
        'django.db.backends.mssql': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'CALL': {
            'handlers': ['debug_file_calls'],
        },
        'STDOUT': {
            'handlers': ['console', 'printed_values'],
        },
        'STDERR': {
            'handlers': ['console', 'printed_values'],
        },
    }
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_rapidjson.renderers.RapidJSONRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_rapidjson.parsers.RapidJSONParser',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
        # 'rest_framework.permissions.IsAuthenticated',  # coockuecutter
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
    'PAGE_SIZE': 100,
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework.authentication.SessionAuthentication',
    #     'rest_framework.authentication.TokenAuthentication',
    # )
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}

# --------------------------------- CACHING STAFF ---------------------------------------

MAX_CACHE_TIME = 60 * 60 * 5
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379?db=0",  # redis is inside docker so we'll not .env it
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.lz4.Lz4Compressor",
            "IGNORE_EXCEPTIONS": True,
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
        },
        'TIMEOUT': MAX_CACHE_TIME,
        "KEY_PREFIX": 'e_logs_cache_',
    }
}

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 60
CACHE_MIDDLEWARE_KEY_PREFIX = ''
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

DJANGO_REDIS_IGNORE_EXCEPTIONS = True
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True

CACHEOPS_REDIS = {
    'host': 'localhost',  # redis-server is on same machine
    'port': 6379,  # default redis port
    'db': 1,  # SELECT non-default redis database
    # using separate redis db or redis instance
    # is highly recommended

    # 'socket_timeout': 3,
}

CACHEOPS_DEFAULTS = {
    'timeout': 60 * 60,
    # 'local_get': True,
}

CACHEOPS = {
    # Automatically cache any User.objects.get() calls for 15 minutes
    # This also includes .first() and .last() calls,
    # as well as request.user or post.author access,
    # where Post.author is a foreign key to auth.User
    'auth.user': {'ops': 'get', 'timeout': 60 * 15},

    # Automatically cache all gets and queryset fetches
    # to other django.contrib.auth models for an hour
    'auth.*': {'ops': {'fetch', 'get'}, 'timeout': 60 * 60},

    # Cache all queries to Permission
    # 'all' is an alias for {'get', 'fetch', 'count', 'aggregate', 'exists'}
    'auth.permission': {'ops': 'all', 'timeout': 60 * 60},

    # Enable manual caching on all other models with default timeout of an hour
    # Use Post.objects.cache().get(...)
    #  or Tags.objects.filter(...).order_by(...).cache()
    # to cache particular ORM request.
    # Invalidation is still automatic
    # '*.*': {'timeout': 60*60},
    '*.*': {'ops': 'all', 'timeout': 60 * 60},

    'core.models.Setting': {'ops': 'all', 'timeout': 60 * 60},
    'common.all_journals_app.models.Cell': {'ops': 'all', 'timeout': 60 * 60},
    'common.all_journals_app.models.Journal': {'ops': 'all', 'timeout': 60 * 60},
    # 'core.models.Setting': {'timeout': 60*60},
    # 'core.models.Setting': {'timeout': 60*60},
}

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE


CORS_ORIGIN_ALLOW_ALL = True
