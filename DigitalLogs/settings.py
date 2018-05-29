"""
Django settings for DigitalLogs project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
    'login_app.apps.LoginApp',
    'leaching.express_anal_app.apps.ExpressAnalApp',
    'leaching.repair_app.apps.LeachingRepairAppConfig',
    'furnace.repair_app.apps.FurnaceRepairAppConfig',
    'furnace.fractional_app.apps.FurnaceFractionalAppConfig',
    'furnace.concentrate_report_app.apps.FurnaceConcentrateReportAppConfig',
    'furnace.loading_shihta_app.apps.FurnaceLoadingShihtaAppConfig',
    'furnace.metals_compute_app.apps.FurnaceMetalsComputeAppConfig',
    'furnace.replaceable_technological_tasks_app.apps.FurnaceReplaceableTechnologicalTasksAppConfig',
    'common.all_journals_app.apps.CommonAllJournalsAppConfig',
    'electrolysis.technical_report_app.apps.TechnicalReportAppConfig'
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
]

ROOT_URLCONF = 'DigitalLogs.urls'

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

            'libraries':{
                    'express_tags': 'leaching.express_anal_app.templatetags.express_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'DigitalLogs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# driver='{ODBC Driver 13 for SQL Server}',
#                           server='WIN-E402USVKBEF',
#                           database='ZincSales_Dev',
#                           username='ZincSales_Dev',
#                           password='Singapore2017',
#                           trusted_connection='yes'
#                           )

# DATABASES = {
#     'default': {
#         'NAME': 'my_database',
#         'ENGINE': 'sqlserver_ado',
#         'HOST': 'dbserver\\ss2012',
#         'USER': '',
#         'PASSWORD': '',
#     }
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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ugettext = lambda s: s
LANGUAGES = (
    ('ru', ugettext('Russian')),
    ('en', ugettext('English')),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

APPEND_SLASH = True

LOGIN_URL = '/auth/login_page'
