from rest_framework import serializers

from box.shop.item.models import (
  Item, ItemFeature, ItemCategory, ItemFeatureCategory, ItemImage, ItemReview,
  Currency
)


class CurrencySerializer(serializers.ModelSerializer):
  class Meta:
    model = Currency
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


class ItemSerializer(serializers.ModelSerializer):
  images   = ItemImageSerializer(many=True, read_only=True)
  features = ItemFeatureSerializer(many=True)
  category = ItemCategorySerializer()
  price    = serializers.ReadOnlyField()
  reviews  = ItemReviewSerializer(many=True)
  currency = CurrencySerializer()
  class Meta:
    model = Item
    exclude = [
    ]

