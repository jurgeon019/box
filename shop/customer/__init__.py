from django import apps 
from django.utils.translation import gettext_lazy as _


class CustomerConfig(apps.AppConfig):
    name = 'box.shop.customer'
    verbose_name = _('Покупці')
    verbose_name_plural = verbose_name
    

default_app_config = 'box.shop.customer.CustomerConfig'

