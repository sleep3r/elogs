import os

from .settings_base import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', '88.99.2.149', 'kzukgs7Elog0.kazzinc.kz', '10.77.103.88', 'elogs.kazzinc.kz']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],

            'libraries': {
                'express_tags': 'common.all_journals_app.templatetags.express_tags',
            }
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'ELogs',
        'HOST': '192.168.22.129',
        'PORT': '',
        'USER': 'admin',
        'PASSWORD': 'Moscow2018',
        'OPTIONS': {
            'driver': 'ODBC Driver 13 for SQL Server',
        },
    },
}


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = True

USE_TZ = True


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
