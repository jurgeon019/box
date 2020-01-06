from rest_framework import serializers
from shop.cart.models import CartItem,  FavourItem
from shop.item.api.serializers import ItemSerializer


class CartItemSerializer(serializers.ModelSerializer):
  item = ItemSerializer()
  total_price = serializers.ReadOnlyField()
  class Meta:
    model = CartItem
    exclude = []


class FavourItemSerializer(serializers.ModelSerializer):
  item = ItemSerializer()
  class Meta:
    model = FavourItem
    exclude = []
