from .settings_base import *


DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'DjangoRelease',
        'HOST': '88.99.2.149',
        'PORT': '',
        'USER': 'InframineDeveloper',
        'PASSWORD': 'Singapore2017',

        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
}
