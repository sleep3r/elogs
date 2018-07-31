"""
Django settings for DigitalLogs project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.conf.global_settings import INTERNAL_IPS

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INTERNAL_IPS = '127.0.0.1'

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

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [BASE_DIR / 'static']


LOCALE_PATHS = [BASE_DIR / 'locale']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u-l(u==u!yqn!5k$a=1-k8zf7!1d2*3a(mxm4ec+a-9-hxduk8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', '88.99.2.149']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webpack_loader',
    'debug_toolbar',
    'django_extensions',
    'migraph',
    'nplusone.ext.django',

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
    'nplusone.ext.django.NPlusOneMiddleware',
    'querycount.middleware.QueryCountMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'e_logs.core.middleware.ExceptionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'querycount.middleware.QueryCountMiddleware',
]

ROOT_URLCONF = 'config.urls'


WSGI_APPLICATION = 'config.wsgi.application'

HTML_MINIFY = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'elogs',
        'HOST': '127.0.0.1',
        'PORT': '1433',
        'USER': 'sa',
        'PASSWORD': 'Singapore2017',

        'OPTIONS': {
            'driver': 'ODBC Driver 13 for SQL Server',
        },
    },
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'sql_server.pyodbc',
#         'NAME': 'DjangoRelease',
#         'HOST': '88.99.2.149',
#         'PORT': '',
#         'USER': 'InframineDeveloper',
#         'PASSWORD': 'Singapore2017',
#
#         'OPTIONS': {
#             'driver': 'ODBC Driver 13 for SQL Server',
#         },
#     },
# }


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = False

USE_L10N = True

USE_TZ = True


def ugettext(s): return s


LANGUAGES = (
    ('ru', ugettext('Russian')),
    ('en', ugettext('English')),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

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
            '()': 'logs.formatters.ColorsFormatter',
            'format': "[%(asctime)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'color_formatter',
        },
        'production_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/main.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_false'],
        },
        'debug_file_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/main_debug_debug.log',
            'maxBytes': 1024 * 1024 * 2,  # 2 MB
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_true'],
        },
        'debug_file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/main_debug_info.log',
            'maxBytes': 1024 * 1024 * 2,  # 2 MB
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_true'],
        },
        'debug_file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/main_debug_error.log',
            'maxBytes': 1024 * 1024 * 2,  # 2 MB
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_true'],
        },
        'debug_file_calls': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/main_debug_calls.log',
            'maxBytes': 1024 * 1024 * 2,  # 2 MB
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_true'],
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
        'werkzeug': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'py.warnings': {
            'handlers': ['console', 'debug_file_debug', 'debug_file_info', 'debug_file_error'],
        },
        '': {
            'handlers': ['production_file', 'debug_file_debug', 'debug_file_info', 'debug_file_error'],
            'level': "DEBUG",
        },
        'django': {
            'handlers': ['console', 'debug_file_debug', 'debug_file_info', 'debug_file_error'],
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
    }
}
