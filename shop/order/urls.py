from django.urls import path 
from shop.order.views  import *


urlpatterns = [
    path("order_items/", order_items, name="order_items"),
]
