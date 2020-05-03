from django.apps import AppConfig 

from django.utils.translation import gettext_lazy as _


class SiteSettingConfig(AppConfig):
    name = 'box.core.sw_global_config'
    verbose_name = _('Налаштування сайту')

default_app_config = 'box.core.sw_global_config.SiteSettingConfig'
