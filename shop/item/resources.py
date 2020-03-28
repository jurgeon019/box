from django.utils import timezone 
from django.conf import settings 
from django.utils.translation import gettext_lazy as _
from django.db.models.query import QuerySet
from django.contrib.sites.models import Site

from import_export.resources import ModelResource
from import_export.fields import Field 
from import_export.widgets import ManyToManyWidget

import tablib

import random
import json 

from .models import * 
from box.core.utils import get_multilingual_fields



class ItemResource(ModelResource):

    class Meta:
        model = Item 
        exclude = [
            'id',
            'created',
            'updated',
            'order',
        ]

    def before_import_row(self, row, **kwargs):
        self.handle_markers_import(row)
        self.handle_similars_import(row)
        self.handle_features_import(row)
        self.handle_manufacturer_import(row)
        self.handle_brand_import(row)
        self.handle_currency_import(row)
        self.handle_category_import(row)
        self.handle_in_stock_import(row)
        self.handle_images_import(row)

    # images  = Field(column_name=_('images') )
    # reviews  = Field(column_name=_('reviews') )
    # variants = Field(column_name=_('variants') )
    # options  = Field(column_name=_('options') )
    # features = Field(column_name=_('features') )

    # m2m 
    # similars = Field(column_name='similars')
    # markers = Field(column_name='markers')
    # markers = Field(column_name="markers", widget=ManyToManyWidget(ItemMarker))
    # markers = Field(column_name="markers", widget=ManyToManyWidget(ItemMarker, field='name'))


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
    
    def handle_markers_import(self, row):
        if row.get('markers'):
            markers = []
            for marker_name in row['markers'].split(','):
                marker, _ = ItemMarker.objects.get_or_create(name=marker_name)
                markers.append(marker.id)
            row['markers'] = ','.join(markers)

    # def dehydrate_markers(self, item):
    #     markers = None 
    #     if item.markers:
    #         markers = ','.join([marker.text for marker in item.markers.all()])
    #     return markers


    def handle_similars_import(self, row):
        if row.get('similars'):
            similars = []
            for pk in row['similars'].split(','):
                similar  = Item.objects.get(pk=pk)
                similars.append(similar.pk)
            row['similars'] = ','.join(similars)

    # def dehydrate_similars(self, item):
    #     similars = None 
    #     if item.similars:
    #         similars = item.similars.all()
    #     return similars.values_list('code', flat=True)


    def handle_features_import(self, row):
        if row.get('features'):
            features = []
            for feature in json.loads(row['features']):
                feature, _ = ItemFeature.objects.get_or_create(code=feature['code'])
                features.append(feature.id)
            row['features'] = features 

    def dehydrate_features(self, item):
        features = []
        count = 0 # 1
        for feature in ItemFeature.objects.all().filter(item=item):
            values = [value.value for value in feature.value.all()]
            features.append({
                'id': feature.id,
                'code':feature.code,
                'name':feature.name.name,
                'values':values,
                # 'feature_value':feature.value.value,
            })
            count += 1 
        return features
    

    def handle_manufacturer_import(self, row):
        if row.get('manufacturer'):
            manufacturer_name   = row['manufacturer']
            manufacturer, _     = ItemManufacturer.objects.get_or_create(name=manufacturer_name)
            row['manufacturer'] = manufacturer.id

    def dehydrate_manufacturer(self, item):
        manufacturer = None 
        if item.manufacturer:
            manufacturer = item.manufacturer.name
        return manufacturer


    def handle_brand_import(self, row):
        if row.get('brand'):
            brand_title  = row['brand']
            brand, _     = ItemBrand.objects.get_or_create(title=brand_title)
            row['brand'] = brand.id

    def dehydrate_brand(self, item):
        brand = None 
        if item.brand:
            brand = item.brand.title
        return brand
        

    def handle_currency_import(self, row):
        if row.get('currency'):
            currency_code   = row['currency']
            currency, _     = ItemCurrency.objects.get_or_create(code=currency_code)
            row['currency'] = currency.id

    def dehydrate_currency(self, item):
        currency = None
        if item.currency: currency = item.currency.code 
        return currency


    def handle_category_import(self, row):
        if row.get('category'):
            category_name = row['category']
            category, _ = ItemCategory.objects.get_or_create(title=category_name)
            row['category'] = category.id

    def dehydrate_category(self, item):
        category = None 
        if item.category: category = item.category.code 
        return category


    def handle_in_stock_import(self, row):
        if row.get('in_stock'):
            in_stock_text   = row['in_stock']
            in_stock, _     = ItemStock.objects.get_or_create(text=in_stock_text)
            row['in_stock'] = in_stock.id
            
    def dehydrate_in_stock(self, item):
        in_stock = None 
        if item.in_stock: in_stock = item.in_stock.text 
        return in_stock


    def handle_images_import(self, row):
        if row.get('images'):
            images = []
            image_names = row['images'].split(',')
            for image_name in image_names:
                image, _ = ItemImage.objects.get_or_create(
                    image=f'shop/items/{image_name}'
                )
                images.append(image.id)
            row['images'] = images 

    def dehydrate_images(self, item):
        images = ItemImage.objects.all().filter(item=item) 
        images_url = ','.join([image.image.url for image in images])
        return images_url


    # def dehydrate_variants(self, item):
    #     variants = ItemVariant.objects.all().filter(item=item)
    #     # if variants.exists:
    #     #     return variants
    #     # return None
    #     return variants.values_list('code', flat=True)    
    #     # return variants
    
    # def dehydrate_reviews(self, item):
    #     reviews = ItemReview.objects.all().filter(item=item)
    #     return reviews.values_list('code', flat=True)
    #     # return reviews

    # # def dehydrate_options(self, item):
    # #     options = ItemOption.objects.all().filter(item=item)
    # #     return options#.values_list('code', flat=True)
    





class ItemCurrencyResource(ModelResource):
    
    class Meta:
        model = ItemCurrency
        exclude = [
            'id',
            'code',
            'order',
            'is_active',
            'created',
            'updated',
        ]
    
    def get_export_order(self):
        multilingual_fields = get_multilingual_fields(self._meta.model)
        order = [
            'is_main',
            'name',
            'code',
            'rate',
            *multilingual_fields['symbol'],
        ]
        return order 
    
    def get_import_id_fields(self):
        import_id_fields = [
            'code',
        ]
        return import_id_fields 
    

