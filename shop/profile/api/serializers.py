from rest_framework import serializers
from box.shop.order.models import Order, Status
from box.shop.cart.api.serializers import CartItemSerializer


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = []
        model = Status


class OrderSerializer(serializers.ModelSerializer):
    status     = StatusSerializer()
    currency   = serializers.ReadOnlyField()
    cart_items = CartItemSerializer(many=True)
    class Meta:
        model = Order 
        exclude = [
            'user',
        ]

