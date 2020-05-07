from django import apps
from django.utils.translation import gettext_lazy as _


class CoreConfig(apps.AppConfig):
    name = 'box.core'
    verbose_name = _('Ядро')
    verbose_name_plural = verbose_name



default_app_config = 'box.core.CoreConfig'


