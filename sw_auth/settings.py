from django.conf import settings 


DEFAULT_LOGIN_REDIRECT_URL = 'customer'



LOGIN_REDIRECT_URL = getattr(settings, 'LOGIN_REDIRECT_URL', DEFAULT_LOGIN_REDIRECT_URL)


