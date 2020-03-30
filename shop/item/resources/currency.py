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
            'is_active',
            'code',
            'old_price',
            'new_price',
            "currency",
            'image',

            "images",
            "features",

            "category",
            "manufacturer",
            "brand",
            "in_stock",
            'amount',
            'units',
            # "markers",
            # "similars",
            # "reviews",
            # "variants",
            # "options",
            # 'slug',
            *multilingual_fields['title'],
            *multilingual_fields['description'],
            *multilingual_fields['alt'],
            *multilingual_fields['meta_title'],
            *multilingual_fields['meta_descr'],
            *multilingual_fields['meta_key'],
        ]
        return order 

    def get_import_id_fields(self):
        fields = [
            # 'slug',
            # 'id',
            'code',
        ]
        return fields 
    
