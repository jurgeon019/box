from import_export.resources import ModelResource
from .models import * 


class GlobalConfigResource(ModelResource):
    class Meta:
        model = GlobalConfig
        exclude = []


class GlobalRecipientEmailResource(ModelResource):
    class Meta:
        model = GlobalRecipientEmail
        exclude = []


class GlobalMarkerResource(ModelResource):
    class Meta:
        model = GlobalMarker
        exclude = []

    def before_import_row(self, row, **kwargs):
        if row.get('code') == '': row['code'] = None


class GlobalLabelResource(ModelResource):
    class Meta:
        model = GlobalLabel
        exclude = []
    
    def before_import_row(self, row, **kwargs):
        if row.get('code') == '': row['code'] = None



