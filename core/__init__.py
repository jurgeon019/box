from django import apps



class CoreConfig(apps.AppConfig):
    name = 'box.core'
    verbose_name = 'Ядро'
    verbose_name_plural = 'Ядро'



default_app_config = 'box.core.CoreConfig'



