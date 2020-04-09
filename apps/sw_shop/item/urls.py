from django.urls import path, include 

urlpatterns = [
  path('', include('box.apps.sw_shop.item.api.urls')),
]
