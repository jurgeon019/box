from django.urls import path, include 

urlpatterns = [
  path('', include('box.apps.sw_shop.sw_item.api.urls')),
]
