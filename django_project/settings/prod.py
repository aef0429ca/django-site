from .base import *

DEBUG = True

ALLOWED_HOSTS = ['49.12.12.34', 'www.endirio.com', 'endirio.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'SKAL123vit',
        'HOST': '127.0.0.1',
        'PORT': 5432,
    }
}