from import_export.resources import ModelResource
from ..models import * 

class ItemManufacturerResource(ModelResource):
    class Meta:
        model = ItemManufacturer
        exclude = []

class ItemUnitResource(ModelResource):
    class Meta:
        model = ItemUnit
        exclude = []

class ItemBrandResource(ModelResource):
    class Meta:
        model = ItemBrand
        exclude = []

class ItemMarkerResource(ModelResource):
    class Meta:
        model = ItemMarker
        exclude = []
    def before_import_row(self, row, **kwargs):
        if row.get('code') == '':
            row['code'] = None

class ItemLabelResource(ModelResource):
    class Meta:
        model = ItemLabel
        exclude = []
    def before_import_row(self, row, **kwargs):
        if row.get('code') == '':
            row['code'] = None

class ItemStockResource(ModelResource):
    class Meta:
        model = ItemStock
        exclude = []
    def before_import_row(self, row, **kwargs):
        if row.get('code') == '':
            row['code'] = None

class ItemImageResource(ModelResource):
    class Meta:
        model = ItemImage
        exclude = [
            'order',
            'created',
            'updated',
        ]
    
    def before_import_row(self, row, **kwargs):
        if row.get('item'):
            row['item'] = Item.objects.get(id=row['item'])
        
        if row.get('code') == '':
            row['code'] = None 
        
        # if row.get('image'):
        #     image = row['image']
        #     image = f'/media/shop/item/{image}'
        #     row['image'] = image
        
    def dehydrate_item(self, image):
        item = None 
        if image.item:
            item = image.item.id
        return item 

    # def dehydrate_image(self, image):
    #     image = image.image.url.replace('/media/shop/item/','')
    #     return image
