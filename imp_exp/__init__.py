from django import apps 


class ImportExportConfig(apps.AppConfig):
    name = 'box.imp_exp'
    verbose_name = 'Імпорт/Експорт'

default_app_config = 'box.imp_exp.ImportExportConfig'


