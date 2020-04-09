from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WayforpayConfig(AppConfig):
    name = 'box.apps.sw_payment.wayforpay'
    verbose_name = _("Wayforpay")
    verbose_name_plural = verbose_name


default_app_config = 'box.apps.sw_payment.wayforpay.WayforpayConfig'



