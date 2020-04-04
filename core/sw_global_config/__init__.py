from django.apps import AppConfig 


class SiteSettingConfig(AppConfig):
    name = 'box.core.sw_global_config'
    verbose_name = 'Налаштування сайту'

default_app_config = 'box.core.sw_global_config.SiteSettingConfig'
