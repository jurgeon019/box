from django import apps 
from django.utils.translation import gettext_lazy as _

class CustomAuthConfig(apps.AppConfig):
    name = 'box.custom_auth'
    verbose_name = _('аккаунти')
    verbose_name_plural = verbose_name

    
    
default_app_config = 'box.custom_auth.CustomAuthConfig'