from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class StarwayConfig(AppConfig):
    name = 'starway'
    verbose_name = _('Старвей')
    verbose_name_plural = _('Старвейы')
    
