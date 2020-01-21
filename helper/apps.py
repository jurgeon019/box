from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class HelperConfig(AppConfig):
    name = 'helper'
    verbose_name = _('Чат')
    verbose_name_plural = _('Чаты')
    
