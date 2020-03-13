from django import apps



class CoreConfig(apps.AppConfig):
    name = 'box.core'
    verbose_name = 'box.core'
    verbose_name_plural = 'box.core'



default_app_config = 'box.core.CoreConfig'



