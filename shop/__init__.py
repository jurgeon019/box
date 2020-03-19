from django import apps 
from django.utils.translation import gettext_lazy as _

class ShopConfig(apps.AppConfig):
    name = 'box.shop'
    verbose_name = _('Магазин')
    verbose_name_plural = verbose_name


default_app_config = 'box.shop.ShopConfig'