from import_export.resources import ModelResource
from .models import OrderStatus, OrderConfig


class OrderStatusResource(ModelResource):
    class Meta:
        model = OrderStatus 
        exclude = []


class OrderConfigResource(ModelResource):
    class Meta:
        model = OrderConfig 
        exclude = []

