from django.apps import AppConfig 


class DesignConfig(AppConfig):
    name = 'box.design'
    verbose_name = 'Дизайн'
    verbose_name_plural = 'Дизайн'

default_app_config = 'box.design.DesignConfig'


