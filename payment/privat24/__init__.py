
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Privat24Config(AppConfig):
    name = 'box.payment.privat24'
    verbose_name = _("privat24")
    verbose_name_plural = verbose_name


default_app_config = 'box.payment.privat24.Privat24Config'


