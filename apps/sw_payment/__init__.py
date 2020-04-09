from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PaymentConfig(AppConfig):
    name = 'box.apps.sw_payment'
    verbose_name = _("Оплата")
    verbose_name_plural = verbose_name


default_app_config = 'box.apps.sw_payment.PaymentConfig'



