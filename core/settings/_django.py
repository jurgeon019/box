import os
import ast
from decouple import config


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SQLITE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}
POSTGRES = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'margo_db',
    'USER' : 'jurgeon018',
    'PASSWORD' : '69018',
    'HOST' : '127.0.0.1',
    'PORT' : '5432',
}
DB = SQLITE
# DB = POSTGRES
DATABASES = {
    'default': DB,
}
# CSRF_COOKIE_HTTPONLY = False 
# ROOT_URLCONF     = 'box.core.urls'
# WSGI_APPLICATION = 'box.core.wsgi.application'
# DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240
ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'custom_auth.User'
SECRET_KEY = config('SECRET_KEY') or 'ss'
DEBUG      = ast.literal_eval(config('DEBUG') or "True")  #python manage.py runserver --insecure # for 404 page
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'
SITE_ID=1
