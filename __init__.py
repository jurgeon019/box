from django.apps import AppConfig


class BoxConfig(AppConfig):
    name = 'box'
    verbose_name = 'Коробка'
    verbose_name_plural = verbose_name


default_app_config = 'box.BoxConfig'

