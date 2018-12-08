import os
import django
import environ

env = environ.Env(DEBUG=(bool, False))


environ.Env.read_env(".env")

DJANGO_SETTINGS_MODULE = env('DJANGO_SETTINGS_MODULE')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)

django.setup()
