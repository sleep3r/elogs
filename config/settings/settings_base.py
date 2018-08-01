import os
import sys
from pathlib import Path

from django.conf.global_settings import INTERNAL_IPS

BASE_DIR = Path(__file__).resolve().parent.parent.parent

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
                'express_tags': 'e_logs.common.all_journals_app.templatetags.express_tags',
            }
        },
    },
]

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / 'static']

LOCALE_PATHS = [BASE_DIR / 'locale']

SECRET_KEY = 'u-l(u==u!yqn!5k$a=1-k8zf7!1d2*3a(mxm4ec+a-9-hxduk8'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', '88.99.2.149']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webpack_loader',
    'django_extensions',

    'e_logs.core.apps.CoreConfig',

    'e_logs.common.login_app.apps.LoginApp',
    'e_logs.common.all_journals_app.apps.CommonAllJournalsAppConfig',
    'e_logs.common.messages_app.apps.CommonMessagesAppConfig',
    'e_logs.common.feedback_app.apps.FeedbackAppConfig',

    # TODO: DELETE THIS APP !!!!!!!!!
    'e_logs.leaching.repair_reports_app.apps.LeachingRepairReportsAppConfig',

    'e_logs.furnace.fractional_app.apps.FurnaceFractionalAppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'e_logs.core.middleware.ExceptionMiddleware',
]

ROOT_URLCONF = 'config.urls'


WSGI_APPLICATION = 'config.wsgi.application'

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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = False

USE_L10N = True

USE_TZ = True

ugettext = lambda s: s
LANGUAGES = (
    ('ru', ugettext('Russian')),
    ('en', ugettext('English')),
)

APPEND_SLASH = True

LOGIN_URL = '/auth/login_page'
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
            'format': "[%(asctime)s] %(message)s",
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
            'filename': 'logs/main.log',
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_false'],
            'when': 'midnight',
        },
        'debug_file_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/main_debug_debug.log',
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_true'],
            'when': 'midnight',
        },
        'debug_file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/main_debug_info.log',
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_true'],
            'when': 'midnight',
        },
        'debug_file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/main_debug_error.log',
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_true'],
            'when': 'midnight',
        },
        'debug_file_calls': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/main_debug_calls.log',
            'backupCount': 7,
            'formatter': 'main_formatter',
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
            'handlers': ['production_file', 'debug_file_debug','debug_file_info', 'debug_file_error'],
            'level': "DEBUG",
        },
        'django': {
            'handlers': ['console','debug_file_debug', 'debug_file_info', 'debug_file_error'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db': {
            'handlers': ['console', 'debug_file_debug', 'debug_file_info', 'debug_file_error'],
            'level': 'INFO',
            'propagate': False,
        },
        'werkzeug': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'CALL': {
            'handlers': ['debug_file_calls'],
        },
        'STDOUT': {
            'handlers': ['console'],
        },
        'STDERR': {
            'handlers': ['console'],
        },
        'django.db.backends': {
            'handlers': ['debug_file_debug'],
            'level': 'INFO',
        }
    }
}
