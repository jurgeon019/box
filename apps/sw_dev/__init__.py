from django.apps import AppConfig



class DevConfig(AppConfig):
    name = 'box.apps.sw_dev'
    verbose_name = 'тестовий магазин'


default_app_config = 'box.apps.sw_dev.DevConfig'