from django.urls import path, include 
from .cart_api import *
from .favours_api import *
from .views import * 

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('cart_items', CartItemViewSet)


old_urlpatterns = [
  path('get_cart_items/',         get_cart_items,          name='get_cart_items'),
  path('add_cart_item/',          add_cart_item,           name='add_cart_item'),
  path('remove_cart_item/',       remove_cart_item,        name='remove_cart_item'),
  path('change_cart_item_amount/',change_cart_item_amount, name='change_cart_item_amount'),
  path('change_item_amount/',     change_item_amount,      name='change_item_amount'),

  path('clear_cart/',             clear_cart,              name='clear_cart'),

  path('get_favours_amount/',     get_favours_amount,      name='get_favours_amount'),
  path('get_favours/',            get_favours,             name='get_favours'),
  path('add_favour/',             add_favour,              name='add_favour'),
  path('remove_favour/',          remove_favour,           name='remove_favour'),
  path('add_favour_to_cart/',     add_favour_to_cart,      name='add_favour_to_cart'),
  path('add_favours_to_cart/',    add_favours_to_cart,     name='add_favours_to_cart'),
  # path('add_favour_by_like/',     add_favour_by_like,      name='add_favour_by_like'),
  path('remove_favour_by_like/',  remove_favour_by_like,   name='remove_favour_by_like'),
]

urlpatterns = [
  path('', include(old_urlpatterns)), 
  path('', include(router.urls)),
]


