from django.apps import AppConfig 


class SiteSettingConfig(AppConfig):
    name = 'box.global_config'
    verbose_name = 'Налаштування сайту'

default_app_config = 'box.global_config.SiteSettingConfig'
