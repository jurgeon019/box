
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NovaPoshtaAppConfig(AppConfig):
    name = 'box.apps.sw_delivery.sw_novaposhta'
    verbose_name = _('Nova poshta')


default_app_config = 'box.apps.sw_delivery.sw_novaposhta.NovaPoshtaAppConfig'



