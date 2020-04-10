from rest_framework import serializers

from box.apps.sw_shop.sw_item.models import (
  Item, ItemFeature, ItemCategory, ItemFeatureCategory, ItemImage, ItemReview,
  ItemCurrency, ItemStock
)

from django.conf import settings 
from box.apps.sw_shop.sw_item import settings as item_settings


class ItemCurrencySerializer(serializers.ModelSerializer):
  class Meta:
    model = ItemCurrency
    exclude = []

class ItemReviewSerializer(serializers.ModelSerializer):
  created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
  updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

  class Meta:
    model = ItemReview
    exclude = []



class ItemFeatureSerializer(serializers.ModelSerializer):
  class Meta:
    model = ItemFeature
    
    exclude = [
      # 'item',
    ]


class ItemFeatureCategorySerializer(serializers.ModelSerializer):
  features = ItemFeatureSerializer(many=True)
  class Meta:
    model = ItemFeatureCategory
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

class ItemSerializer(serializers.ModelSerializer):
  images   = ItemImageSerializer(many=True, read_only=True)
  features = ItemFeatureSerializer(many=True)
  full_url = serializers.SerializerMethodField() 
  def get_full_url(self, obj):
      return obj.get_absolute_url()

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
    exclude = []

