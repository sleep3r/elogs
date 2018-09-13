import faulthandler

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

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'template_profiler_panel.panels.template.TemplateProfilerPanel',
]

CACHEOPS_ENABLED = True

faulthandler.enable()
