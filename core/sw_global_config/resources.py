from import_export.resources import ModelResource
from .models import * 



class GlobalConfigResource(ModelResource):
    class Meta:
        model = GlobalConfig
        exclude = []
