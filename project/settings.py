INSTALLED_APPS = [
    'filebrowser',
    'modeltranslation',
    'custom_admin.apps.CustomAdminConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.redirects',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    # custom

    'blog.apps.BlogConfig',

    'shop.apps.ShopConfig',
    'shop.test_shop.apps.TestShopConfig',
    'shop.item.apps.ItemConfig',
    'shop.order.apps.OrderConfig',
    'shop.cart.apps.CartConfig',
    'shop.liqpay.apps.LiqpayConfig',
    'shop.privat24.apps.Privat24Config',
    'shop.profile.apps.ProfileConfig',

    'pages.apps.PageConfig',

    'custom_auth.apps.CustomAuthConfig',

    'project.apps.ProjectConfig',

    'forms.apps.FormsConfig',

    # third-party
    "crispy_forms",
    "tinymce",
    'ckeditor',
    'ckeditor_uploader',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'import_export',
    'rosetta',
    'django_celery_beat',
]
############################################
# mail-stuff
# config = RawConfigParser()
# config.read('/home/jurgeon/dev/margo/settings.ini')
# config.read('../../settings.ini')
# EMAIL_HOST_USER     = config.get('section', 'jurgeon_EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config.get('section', 'jurgeon_EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = "jurgeon018@gmail.com"
EMAIL_HOST_PASSWORD = "yfpfhrj69008"
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True
# EMAIL_HOST_USER     = config.get('section', 'margo_EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config.get('section', 'margo_EMAIL_HOST_PASSWORD')
# EMAIL_HOST          = 'mail.adm.tools'
# EMAIL_PORT          = 25
# EMAIL_USE_TLS       = False
# EMAIL_USE_SSL       = False
# print(EMAIL_HOST_PASSWORD, EMAIL_HOST_USER)
DEFAULT_FROM_EMAIL = 'Margo Site Team <info@margoltd.com>'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

############################################
# celery-stuff
# REDIS_HOST = 'localhost'
# REDIS_PORT = '6379'
# BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
# BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600} 
# CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
# CELERY_TIMEZONE = 'Asia/Makassar'
CELERY_BROKER_URL = 'amqp://127.0.0.1//'
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379//'
# CELERY_ACCEPT_CONTENT = ['json']
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULE = {
    # 'third-task':{
    #     'task':'app1.tasks.task_three',
    #     'schedule': 2.0,
    #     # 'args': 
    # },
    # 'fourth-task':{
    #     'task':'app1.tasks.task_four',
    #     'schedule': 3.0,
    #     # 'args': 
    # },
    # 'fifth-task':{
    #     'task':'app1.tasks.task_five',
    #     'schedule': crontab(minute=59, hour=23),
    #     # 'schedule': crontab(minute=0, hour='*/3,10-19'),
    #     # 'schedule': crontab(hour=16, day_of_week=5),
    #     # 'schedule': 3600.0,
    #     # 'schedule': solar('sunset', -37.81753, 144.96715),
    # },
    # 'sixth-task':{
    #     'task':'app1.tasks.task_six',
    #     'schedule':3.0
    # }

}
from celery.schedules import crontab
from datetime import timedelta
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Asia/Makassar'
CELERY_BEAT_SCHEDULE = {
  'task_one':{
    'task':'blog.tasks.task_number_one',
    # 'schedule':crontab(minute=59, hour=23),
    "schedule": timedelta(seconds=2),
    # 'args':(*args),
  },
  'task_two':{
    'task':'blog.tasks.task_number_two',
    # 'schedule':crontab(minute=0, hour='*/3,10-19'),
    "schedule": timedelta(seconds=2),
    # 'args':(*args),
  }
}

###########################################
# django-stuff
import os
from decouple import config
from django.utils.translation import ugettext_lazy as _
import allauth 
from configparser import RawConfigParser
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'shop.cart.context_processors.cart_content',
                'shop.item.context_processors.categories',
            ],
        },
    },
]
# DEBUG = False   #python manage.py runserver --insecure # for 404 page
ACCOUNT_LOGOUT_ON_GET = True 
DEBUG = True   
ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'custom_auth.User'
CURRENT_DOMEN = config('CURRENT_DOMEN', 'margoltd.com') 
SECRET_KEY = config('SECRET_KEY') or 'ss'
DEBUG      = config('DEBUG') or True
ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'
TIME_ZONE = 'UTC' #'Europe/Kiev'
USE_L10N = True
USE_I18N = True
USE_TZ = True
LANGUAGES = (
  ('ru', _('Russian')),
  ('en', _('English')),
  ('uk', _('Ukrainian')),
)
LANGUAGE_CODE = 'uk'
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'
CKEDITOR_UPLOAD_PATH = ''
LOGIN_REDIRECT_URL = 'profile'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
SITE_ID=1
MODELTRANSLATION_DEFAULT_LANGUAGE = 'uk'
ROSETTA_MESSAGES_PER_PAGE = 100
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)
LIQPAY_PUBLIC_KEY = "sandbox_i29048427621"
LIQPAY_PRIVATE_KEY = "sandbox_RBR5FM04gXXt25MLzVmP7eyarKDWIKXw86MEMkvm"
# LIQPAY_PUBLIC_KEY = "i3466565002"
# LIQPAY_PRIVATE_KEY="85pd0UjyxXThv8RQpmPld4Z406wGZF4huAfqDHaB"
#################################
#  other-stuff
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]




