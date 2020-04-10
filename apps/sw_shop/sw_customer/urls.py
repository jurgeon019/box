from django.urls import path, include 



urlpatterns = [
  path('', include('box.apps.sw_shop.sw_customer.api.urls')),  
  path('api/', include('box.apps.sw_shop.sw_customer.api.urls')),  
]
