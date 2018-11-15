import faulthandler

from .settings_base import *

DEBUG = True
INTERNAL_IPS = ['127.0.0.1', '10.0.2.2']

INSTALLED_APPS += [
    'migraph',
    'nplusone.ext.django',
    'hijack',
    'compat',
    'debug_toolbar',
    'template_profiler_panel',
]

MIDDLEWARE = [
                 'djdev_panel.middleware.DebugMiddleware',
                 'nplusone.ext.django.NPlusOneMiddleware',
                 'querycount.middleware.QueryCountMiddleware',
             ] + MIDDLEWARE + \
             [
                 'debug_toolbar.middleware.DebugToolbarMiddleware',
                 'querycount.middleware.QueryCountMiddleware',
             ]

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

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

CACHEOPS_ENABLED = True
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

faulthandler.enable()
