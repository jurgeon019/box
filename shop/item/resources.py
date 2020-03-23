from django.utils import timezone 
from django.conf import settings 
from django.utils.translation import gettext_lazy as _
from django.db.models.query import QuerySet
from django.contrib.sites.models import Site

from import_export.resources import ModelResource
from import_export.fields import Field 

import tablib

import random

from .models import * 
from box.core.utils import get_multilingual_fields



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
            'iso',
            'rate',
            *multilingual_fields['symbol'],
        ]
        return order 
    
    def get_import_id_fields(self):
        import_id_fields = [
            'iso',
        ]
        return import_id_fields 
    














# https://stackoverflow.com/questions/33608952/django-import-export-fields
# _choice_fields = [
#     'field_a', 'field_b',
# ]
# for _field_name in _choice_fields:
#     locals()[_field_name] = import_export.fields.Field(
#         attribute='get_%s_display' % _field_name,
#         column_name=MyModel._meta.get_field(_field_name).verbose_name
#     )



class CustomTablib(tablib.Dataset):
    pass
    # def _validate(self, row=None, col=None, safety=True):
    #     return super()._validate(row, col, safety)

class ItemResource(ModelResource):
    images  = Field(column_name=_('images') )
    remote_images_url = Field(column_name=_('remote_images_url') )
    reviews  = Field(column_name=_('reviews') )
    variants = Field(column_name=_('variants') )
    # options  = Field(column_name=_('options') )
    features = Field(column_name=_('features') )

    class Meta:
        model = Item 
        exclude = [
            'id',
            'created',
            'updated',
            'order',
        ]


    def get_export_order(self):
        multilingual_fields = get_multilingual_fields(self._meta.model)
        order = [
            *multilingual_fields['title'],
            *multilingual_fields['description'],
            'old_price',
            'new_price',
            'amount',
            'units',
            'code',
            'image',
            'is_active',
            'slug',
            *multilingual_fields['alt'],
            *multilingual_fields['meta_title'],
            *multilingual_fields['meta_descr'],
            *multilingual_fields['meta_key'],

            "images",
            "features",
            # "reviews",
            # "variants",
            # "options",

            "category",
            "markers",
            # "similars",
            "manufacturer",
            "brand",
            "in_stock",
            "currency",
        ]
        return order 

    def get_import_id_fields(self):
        fields = [
            'slug',
            'code',
        ]
        return fields 


    # related
    def dehydrate_variants(self, item):
        variants = ItemVariant.objects.all().filter(item=item)
        # if variants.exists:
        #     return variants
        # return None
        return variants.values_list('code', flat=True)    
        # return variants

    def dehydrate_images(self, item):
        images = ItemImage.objects.all().filter(item=item) 
        images_url = ','.join([image.image.url for image in images])
        return images_url

    def dehydrate_reviews(self, item):
        reviews = ItemReview.objects.all().filter(item=item)
        return reviews.values_list('code', flat=True)
        # return reviews

    # def dehydrate_options(self, item):
    #     options = ItemOption.objects.all().filter(item=item)
    #     return options#.values_list('code', flat=True)

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


    # m2m 
    def dehydrate_markers(self, item):
        markers = None 
        if item.markers:
            markers = ','.join([marker.text for marker in item.markers.all()])
        return markers

    def dehydrate_similars(self, item):
        similars = None 
        if item.similars:
            similars = item.similars.all()
        return similars.values_list('code', flat=True)
        # return similars

    # fk
    def dehydrate_manufacturer(self, item):
        manufacturer = None 
        if item.manufacturer:
            manufacturer = item.manufacturer.code
        return manufacturer

    def dehydrate_brand(self, item):
        brand = None 
        if item.brand:
            brand = item.brand.code
        return brand

    def dehydrate_currency(self, item):
        currency = None
        if item.currency:
            currency = item.currency.code 
        return currency
    
    def dehydrate_category(self, item):
        category = None 
        if item.category:
            category = item.category.code 
        return category

    def dehydrate_in_stock(self, item):
        in_stock = None 
        if item.in_stock:
            in_stock = item.in_stock.code 
        return in_stock




