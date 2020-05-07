from import_export.resources import ModelResource
from .models import * 


class LiqpayConfigResource(ModelResource):
    class Meta:
        model = LiqpayConfig 
        exclude = []


