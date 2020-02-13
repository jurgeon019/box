import os
from decouple import config
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
#     'default':{
#       'ENGINE': 'django.db.backends.postgresql_psycopg2',
#       'NAME': 'margo_db',
#       'USER' : 'jurgeon018',
#       'PASSWORD' : '69018',
#       'HOST' : '127.0.0.1',
#       'PORT' : '5432',
#   }
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240
ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'custom_auth.User'
CURRENT_DOMEN = config('CURRENT_DOMEN', 'margoltd.com') 
SECRET_KEY = config('SECRET_KEY') or 'ss'
DEBUG = True   
# DEBUG = False   #python manage.py runserver --insecure # for 404 page
DEBUG      = config('DEBUG') or True
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'
CKEDITOR_UPLOAD_PATH = ''
LOGIN_REDIRECT_URL = 'profile'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
SITE_ID=1
ACCOUNT_LOGOUT_ON_GET = True
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)
# LIQPAY_PUBLIC_KEY = "sandbox_i29048427621"
# LIQPAY_PRIVATE_KEY = "sandbox_RBR5FM04gXXt25MLzVmP7eyarKDWIKXw86MEMkvm"
# LIQPAY_PUBLIC_KEY = "i3466565002"
# LIQPAY_PRIVATE_KEY="85pd0UjyxXThv8RQpmPld4Z406wGZF4huAfqDHaB"
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
# ]
MULTIPLE_CATEGORY = False 







WPADMIN = {
    'admin': {
        # 'admin_site': 'test_project.admin.admin',
        # 'admin_site': 'django.contrib.admin.sites.site',

        'title': 'Django admin panel',
        'menu': {
            # 'top': 'wpadmin.menu.menus.BasicTopMenu',
            'left': 'wpadmin.menu.menus.BasicLeftMenu',
        },
        'dashboard': {
            'breadcrumbs': True,
        },
        # 'custom_style': STATIC_URL + 'wpadmin/css/themes/sunrise.css',
    }
}
