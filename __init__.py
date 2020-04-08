from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.conf import settings 


class BoxConfig(AppConfig):
    name = 'box'
    verbose_name = _('Коробка')
    verbose_name_plural = verbose_name


default_app_config = 'box.BoxConfig'



# if 'box.shop.item' in settings.INSTALLED_APPS:
#     from box.shop.item import * 
# TODO: опреділити, чого воно дає помилку з SECRET_KEY 

