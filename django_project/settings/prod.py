from .base import *

DEBUG = False

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
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# django-site

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/srv/django-site/django_project/static/')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DOC_ROOT = os.path.join(MEDIA_ROOT, 'documents')

MEDIA_URL = '/media/'
DOC_URL = '/documents/'
PROFILE_URL = '/media/documents/profiles/'

TMP_PATH = os.path.join(MEDIA_ROOT, 'documents/tmp')
FINAL_PATH = os.path.join(MEDIA_ROOT, 'documents/final')
TAGS_PATH = os.path.join(BASE_DIR, 'xmltools/config/tags')
XSD_PATH = os.path.join(BASE_DIR, 'xmltools/config/xsd')
XMLSCHEMA_LOG_PATH = os.path.join(BASE_DIR, 'xmltools/config/logs')
PROFILE_PATH = os.path.join(MEDIA_ROOT, 'documents/profiles')