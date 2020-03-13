from box.settings import * 

INSTALLED_APPS.extend([
    'project',
])
CURRENT_DOMEN = 'jcbservice.com.ua'
AUTH_USER_MODEL = 'project.User'
EMAIL_HOST_USER = "admin@jcbservice.com.ua"
EMAIL_HOST_PASSWORD = "jcb69018"
# EMAIL_HOST_USER = 'jurgeon018@gmail.com'
# EMAIL_HOST_PASSWORD = 'yfpfhrj69001'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

