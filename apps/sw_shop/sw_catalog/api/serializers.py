from rest_framework import serializers

from box.apps.sw_shop.sw_catalog.models import *

from django.conf import settings 
from box.apps.sw_shop.sw_catalog import settings as item_settings


class ItemCurrencySerializer(serializers.ModelSerializer):
  class Meta:
    model = ItemCurrency
    exclude = []


class ItemReviewSerializer(serializers.ModelSerializer):
  created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
  updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

  class Meta:
    model = ItemReview
    exclude = [
    ]


class ItemImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = ItemImage
    exclude = [
      'item',
    ]


class ItemSubcategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = ItemCategory
    exclude = []


class ItemCategorySerializer(serializers.ModelSerializer):
  parent = ItemSubcategorySerializer()
  class Meta:
    model = ItemCategory
    exclude = []

class ItemStockSerializer(serializers.ModelSerializer):
  class Meta:
    model = ItemStock 
    exclude = []

class ItemDetailSerializer(serializers.ModelSerializer):
  images   = ItemImageSerializer(many=True, read_only=True)
  # features = ItemFeatureSerializer(many=True)
  absolute_url = serializers.SerializerMethodField() 
  image_url = serializers.SerializerMethodField() 
  
  def get_absolute_url(self, obj):
      return obj.get_absolute_url()

  def get_image_url(self, obj):
    return obj.image_url

  if item_settings.MULTIPLE_CATEGORY:
    categories = ItemCategorySerializer(many=True)
  else:
    category = ItemCategorySerializer()

  price    = serializers.ReadOnlyField()
  reviews  = ItemReviewSerializer(many=True)
  currency = ItemCurrencySerializer()
  in_stock = ItemStockSerializer()

  class Meta:
    model = Item
    exclude = [
      'similars',
      # 'images',
    ]

from django.conf import settings
from modeltranslation.manager import get_translatable_fields_for_model
from rest_framework import serializers



class ItemListSerializer(serializers.ModelSerializer):
  price    = serializers.ReadOnlyField()
  currency = ItemCurrencySerializer()
  in_stock = ItemStockSerializer()

  absolute_url = serializers.SerializerMethodField() 
  def get_absolute_url(self, obj):
      return obj.get_absolute_url()

  image_url = serializers.SerializerMethodField() 
  def get_image_url(self, obj):
    return obj.image_url

  class Meta:
    model = Item
    exclude = [
    ]

  # def get_field_names(self, declared_fields, info):
  #   fields = super().get_field_names(declared_fields, info)
  #   trans_fields = get_translatable_fields_for_model(self.Meta.model)
  #   all_fields = []


  #   requested_langs = []
  #   if 'request' in self.context:
  #     lang_param = self.context['request'].query_params.get('lang', None)
  #     print("lang_param:", lang_param)
  #     requested_langs = lang_param.split(',') if lang_param else []
  #     print("requested_langs:", requested_langs)

  #   for f in fields:
  #     if f not in trans_fields:
  #         all_fields.append(f)
  #     else:
  #         for l in settings.LANGUAGES:
  #             if not requested_langs or l[0] in requested_langs:
  #                 all_fields.append("{}_{}".format(f, l[0]))
  #   print("all_fields:", all_fields)
  #   print()
  #   print("fields:", fields)
  #   print()
  #   print("trans_fields:", trans_fields)
  #   print()

  #   return all_fields

