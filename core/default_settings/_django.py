import os
import ast
from decouple import config
import decouple 


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# AUTH_USER_MODEL = 'project.ProjectUser'
# CSRF_COOKIE_HTTPONLY = False 
# DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240
ROOT_URLCONF     = 'box.core.urls'
WSGI_APPLICATION = 'box.core.wsgi.application'
ALLOWED_HOSTS    = ['*']
SECRET_KEY       = config('SECRET_KEY') or 'ss'
DEBUG            = ast.literal_eval(config('DEBUG') or "True")  #python manage.py runserver --insecure # for 404 page
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT      = os.path.join(BASE_DIR, "static_root")
MEDIA_ROOT       = os.path.join(BASE_DIR, "media")
STATIC_URL       = '/static/'
MEDIA_URL        = '/media/'
SITE_ID          = 1
SQLITE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}
POSTGRES = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'NAME',
    'USER' : 'USER',
    'PASSWORD' : 'PASSWORD',
    'HOST' : '127.0.0.1',
    'PORT' : '5432',
}
DATABASES = {
    'default': SQLITE,
}




