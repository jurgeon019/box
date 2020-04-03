from rest_framework import serializers
from box.sw_shop.cart.models import CartItem,  FavourItem
from box.sw_shop.item.api.serializers import ItemSerializer


class CartItemSerializer(serializers.ModelSerializer):
  item = ItemSerializer()
  total_price = serializers.ReadOnlyField()
  currency = serializers.ReadOnlyField()
  class Meta:
    model = CartItem
    exclude = []


class FavourItemSerializer(serializers.ModelSerializer):
  item = ItemSerializer()
  class Meta:
    model = FavourItem
    exclude = []