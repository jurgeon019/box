import os
import ast
from decouple import config

INTERNAL_IPS = [
    '127.0.0.1',
]
ROOT_URLCONF       = 'box.core.urls'
WSGI_APPLICATION   = 'box.core.wsgi.application'
BASE_DIR           = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ALLOWED_HOSTS      = ['*']
SECRET_KEY         = config('SECRET_KEY') # = ast.literal_eval(config('DEBUG') or "True")  #python manage.py runserver --insecure # for 404 page
DEBUG              = config('DEBUG', cast=bool) # = ast.literal_eval(config('DEBUG') or "True")  #python manage.py runserver --insecure # for 404 page
STATICFILES_DIRS   = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT        = os.path.join(BASE_DIR, "static_root")
MEDIA_ROOT         = os.path.join(BASE_DIR, "media")
STATIC_URL         = '/static/'
MEDIA_URL          = '/media/'
SITE_ID            = 1
LOGIN_REDIRECT_URL = '/profile/' # '/' # 
LOGIN_URL          = '/' # '/login/' #  'profile #
# https://stackoverflow.com/questions/47585583/the-number-of-get-post-parameters-exceeded-settings-data-upload-max-number-field
# DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240 








