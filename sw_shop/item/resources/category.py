from django.utils.translation import gettext_lazy as _

from import_export.resources import ModelResource
from import_export.fields import Field 
from import_export.widgets import ForeignKeyWidget

import json 

from ..models import * 
from box.core.utils import get_multilingual_fields




class ItemCategoryResource(ModelResource):
    parent = Field(
        column_name='parent',
        attribute="parent",
        widget=ForeignKeyWidget(ItemCategory, field='id')
    )
    currency = Field(
        column_name='currency',
        attribute="currency",
        widget=ForeignKeyWidget(ItemCurrency, field='code')
    )
    class Meta:
        model = ItemCategory 
        exclude = [
            'created',
            'updated',
            'order',
            'lft',
            'rght',
            'tree_id',
            'level',
        ]

    def get_export_order(self):
        multilingual_fields = get_multilingual_fields(self._meta.model)
        order = [
            'is_active',
            'id',
            'parent',
            "currency",
            'image',
            'title',
            # *multilingual_fields['title'],
            *multilingual_fields['description'],
            *multilingual_fields['alt'],
            *multilingual_fields['meta_title'],
            *multilingual_fields['meta_descr'],
            *multilingual_fields['meta_key'],
        ]
        return order 
    
    def before_import_row(self, row, **kwargs):
        self.handle_image_import(row)
    
    def handle_image_import(self, row):
        if row.get('image'):
            image = row.get('image')
            row['image'] = f'shop/category/{image}'
    
    def dehydrate_image(self, category):
        image = None 
        # if category.image: image = f'{category.image.url}'.replace('/media/shop/category/','')
        if category.image: image = f'{category.image.url}'.split('/')[-1]
        return image 







