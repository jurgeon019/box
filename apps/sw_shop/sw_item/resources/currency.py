from django.utils.translation import gettext_lazy as _

from import_export.resources import ModelResource
from import_export.fields import Field 


import json 

from ..models import * 
from box.core.utils import get_multilingual_fields



class ItemCurrencyResource(ModelResource):
    
    class Meta:
        model = ItemCurrency
        exclude = [
            'id',
            # 'code',
            'order',
            'is_active',
            'created',
            'updated',
        ]

    def get_export_order(self):
        multilingual_fields = get_multilingual_fields(self._meta.model)
        order = [
            "name",
            "symbol",
            "code",
            "rate",
            "is_main",
            *multilingual_fields['symbol'],
        ]
        return order 

    def get_import_id_fields(self):
        fields = [
            # 'slug',
            # 'id',
            'code',
        ]
        return fields 
    
