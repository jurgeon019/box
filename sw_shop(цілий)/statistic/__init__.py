from django import apps 


class StaticticConfig(apps.AppConfig):
    name = 'box.statistic'
    verbose_name = 'Статистика'

default_app_config = 'box.statistic.StaticticConfig'


