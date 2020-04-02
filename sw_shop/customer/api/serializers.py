from rest_framework import serializers
from box.sw_shop.order.models import Order, Status
from box.sw_shop.cart.api.serializers import CartItemSerializer


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = []
        model = Status


class OrderSerializer(serializers.ModelSerializer):
    status     = StatusSerializer()
    currency   = serializers.ReadOnlyField()
    created    = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated    = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    cart_items = CartItemSerializer(many=True)
    class Meta:
        model = Order 
        exclude = [
            'user',
        ]

