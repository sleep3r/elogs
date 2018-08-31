from .settings_base import *

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

INSTALLED_APPS += ['gunicorn']

MIDDLEWARE = [] + MIDDLEWARE + \
             [
                 'htmlmin.middleware.HtmlMinifyMiddleware',
                 'htmlmin.middleware.MarkRequestMiddleware',
             ]

HTML_MINIFY = True
