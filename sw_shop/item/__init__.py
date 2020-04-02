from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ItemConfig(AppConfig):
    name = 'box.sw_shop.item'
    verbose_name = _('магазин')
    verbose_name_plural = verbose_name


default_app_config = 'box.sw_shop.item.ItemConfig'
