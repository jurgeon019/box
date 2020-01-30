
from django.urls import path 
from .views import * 


urlpatterns = [
    path('shop/',            shop,     name='test_shop'),
    path('item/<slug>/',     item,     name='test_item'),
    path('category/<slug>/', category, name='test_category'),
    path('order/',           order,    name='test_order'),
    path('mail/', mail, name="test_mail"),
]