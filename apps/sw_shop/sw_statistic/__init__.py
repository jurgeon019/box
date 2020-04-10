from django import apps 


class StaticticConfig(apps.AppConfig):
    name = 'box.apps.sw_show.sw_statistic'
    verbose_name = 'Статистика'

default_app_config = 'box.apps.sw_shop.sw_statistic.StaticticConfig'


