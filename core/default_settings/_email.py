
import re 
from decouple import config 


IGNORABLE_404_URLS = [
    re.compile(r'\.(php|cgi)$'),
    re.compile(r'^/phpmyadmin/'),
]
MAIL_TYPE = config('MAIL_TYPE')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT    = 587
EMAIL_HOST    = "mail.starwayua.com"
EMAIL_HOST_USER = "dev@starwayua.com"
EMAIL_HOST_PASSWORD = "dev69018"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
DEFAULT_RECIPIENT_LIST = [
    'jurgeon018@gmail.com',
]
SERVER_EMAIL = 'dev@starwayua.com'
ADMINS = [
    ('jurgeon018', 'jurgeon018@gmail.com'),
]
MANAGERS = [
    'jurgeon018@gmail.com',
]
if MAIL_TYPE == 'from_settings':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'box.global_config.backends.ConfiguredEmailBackend'


