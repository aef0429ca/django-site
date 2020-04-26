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

# Paths
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# django-site

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/'),]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DOC_URL = '/documents/'
DOC_ROOT = os.path.join(BASE_DIR, '../media/documents')
TMP_PATH = os.path.join(BASE_DIR, '../media/documents/tmp')
FINAL_PATH = os.path.join(BASE_DIR, '../media/documents/final')
XSD_PATH = os.path.join(BASE_DIR, '../xmltools/config/xsd')