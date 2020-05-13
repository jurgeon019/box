
from django.apps import AppConfig as AppConf 

class WatermarkSettings(AppConf):
    name = 'box.core.sw_watermarker'



default_app_config = 'box.core.sw_watermarker.WatermarkSettings'


