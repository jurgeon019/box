from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class BoxConfig(AppConfig):
    name = 'box'
    verbose_name = _('Коробка')
    verbose_name_plural = verbose_name


default_app_config = 'box.BoxConfig'

