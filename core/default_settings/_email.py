import re 
from decouple import config 

MAIL_TYPE = config('MAIL_TYPE')
if MAIL_TYPE == 'from_settings':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'box.core.sw_global_config.backends.ConfiguredEmailBackend'
EMAIL_USE_TLS          = True
EMAIL_USE_SSL          = False
EMAIL_PORT             = 587
EMAIL_HOST             = "mail.starwayua.com"
EMAIL_HOST_USER        = "dev@starwayua.com"
EMAIL_HOST_PASSWORD    = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL     = EMAIL_HOST_USER
DEFAULT_RECIPIENT_LIST = [
    'jurgeon018@gmail.com',
]




# IGNORABLE_404_URLS = [
#     re.compile(r'\.(php|cgi)$'),
#     re.compile(r'^/phpmyadmin/'),
# ]
# SERVER_EMAIL = 'dev@starwayua.com'
# ADMINS = [
#     ('jurgeon018', 'jurgeon018@gmail.com'),
# ]
# MANAGERS = [
#     'jurgeon018@gmail.com',
# ]