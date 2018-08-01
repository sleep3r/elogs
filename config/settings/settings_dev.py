import faulthandler
import ipdb

from .settings_base import *

DEBUG = True
INTERNAL_IPS = '127.0.0.1'

INSTALLED_APPS += ['debug_toolbar',
                   'migraph',
                   'nplusone.ext.django', ]

MIDDLEWARE = [
                 'djdev_panel.middleware.DebugMiddleware',
                 'nplusone.ext.django.NPlusOneMiddleware',
                 'querycount.middleware.QueryCountMiddleware'
             ] + MIDDLEWARE + \
             [
                 'debug_toolbar.middleware.DebugToolbarMiddleware',
                 'querycount.middleware.QueryCountMiddleware'
             ]

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

faulthandler.enable()
# ipdb.set_trace()
