from django import apps 
from django.utils.translation import gettext_lazy as _

class ShopConfig(apps.AppConfig):
    name = 'box.sw_shop'
    verbose_name = _('Магазин')
    verbose_name_plural = verbose_name


default_app_config = 'box.sw_shop.ShopConfig'