from .base import *

DEBUG = True

ALLOWED_HOSTS = ['49.12.12.34', 'www.endirio.com', 'endirio.com']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'SKAL123vit',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
