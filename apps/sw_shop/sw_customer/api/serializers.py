from rest_framework import serializers
from box.apps.sw_shop.sw_order.models import Order, OrderStatus
from box.apps.sw_shop.sw_cart.api.serializers import CartItemSerializer
from ..models import * 

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = []
        model = OrderStatus


class OrderSerializer(serializers.ModelSerializer):
    status     = OrderStatusSerializer()
    currency   = serializers.ReadOnlyField()
    created    = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated    = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    cart_items = CartItemSerializer(many=True)
    class Meta:
        model = Order 
        exclude = [
            'user',
        ]

class CustomerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerGroup
        exclude = []


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        exclude = []


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        exclude = []

