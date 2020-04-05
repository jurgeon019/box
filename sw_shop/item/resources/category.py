from django.utils.translation import gettext_lazy as _

from import_export.resources import ModelResource
from import_export.fields import Field 


import json 

from ..models import * 
from box.core.utils import get_multilingual_fields

from import_export.widgets import ForeignKeyWidget



class ItemCategoryResource(ModelResource):
    # parent = Field(
    #     column_name='parent',
    #     attribute="parent",
    #     widget=ForeignKeyWidget(ItemCategory, field='id')
    # )

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
    def get_import_id_fields(self):
        fields = [
            'id',         
        ]
        return fields 



    def get_export_order(self):
        multilingual_fields = get_multilingual_fields(self._meta.model)
        order = [
            'is_active',
            'id',
            'parent',
            "currency",
            'image',
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
            'id',         
        ]
        return fields 
    
    def before_import_row(self, row, **kwargs):
        # self.handle_parent_import(row)
        self.handle_image_import(row)
    
    def handle_image_import(self, row):
        if row.get('image'):
            image = row.get('image')
            row['image'] = f'shop/category/{image}'
    
    def handle_parent_import(self, row):
        if row.get('parent'):
            parent        = row['parent']
            print(parent)
            parent        = ItemCategory.objects.get(id=parent)
            row['parent'] = parent.id

    def dehydrate_parent(self, category):
        parent = None 
        if category.parent: parent = category.parent.id
        return parent 

    def dehydrate_image(self, category):
        image = None 
        # if category.image: image = f'{category.image.url}'.replace('/media/shop/category/','')
        if category.image: image = f'{category.image.url}'.split('/')[-1]
        return image 







