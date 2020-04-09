from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InterkassaConfig(AppConfig):
    name = 'box.apps.sw_payment.interkassa'
    verbose_name = _("Оплата")
    verbose_name_plural = verbose_name


default_app_config = 'box.apps.sw_payment.interkassa.InterkassaConfig'



