from django.urls import path, include 



urlpatterns = [
  path('', include('box.sw_shop.order.api.urls')),
]
