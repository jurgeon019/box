
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NovaPoshtaAppConfig(AppConfig):
    name = 'box.shop.novaposhta'
    verbose_name = _('Nova poshta')


default_app_config = 'box.shop.novaposhta.NovaPoshtaAppConfig'



