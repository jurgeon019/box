from django.urls import path, include 



urlpatterns = [
  path('', include('box.sw_shop.customer.api.urls')),  
]
