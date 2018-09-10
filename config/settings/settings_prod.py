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

TEMPLATES[0]['APP_DIRS'] = False

INSTALLED_APPS += ['gunicorn', 'whitenoise.runserver_nostatic']


MIDDLEWARE.insert(1, 'django.middleware.gzip.GZipMiddleware')
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

MIDDLEWARE = [] + MIDDLEWARE + \
             [
                 'htmlmin.middleware.HtmlMinifyMiddleware',
                 'htmlmin.middleware.MarkRequestMiddleware',
             ]
HTML_MINIFY = True
