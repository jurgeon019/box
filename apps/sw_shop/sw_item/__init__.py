from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ItemConfig(AppConfig):
    name = 'box.apps.sw_shop.sw_item'
    verbose_name = _('магазин')
    verbose_name_plural = verbose_name


default_app_config = 'box.apps.sw_shop.sw_item.ItemConfig'
