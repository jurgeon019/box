from django.urls import path 
from .views  import *


urlpatterns = [
  path("order_items/", order_items, name="order_items"),
  path('order_request/',  order_request,  name="order_request"),
]