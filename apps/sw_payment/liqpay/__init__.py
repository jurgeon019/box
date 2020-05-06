from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LiqpayConfig(AppConfig):
    name = 'box.apps.sw_payment.liqpay'
    verbose_name = _("Liqpay")
    verbose_name_plural = verbose_name


default_app_config = 'box.apps.sw_payment.liqpay.LiqpayConfig'


