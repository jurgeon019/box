from django.urls import path, include 



urlpatterns = [
  path('', include('box.apps.sw_shop.customer.api.urls')),  
  path('api/', include('box.apps.sw_shop.customer.api.urls')),  
]
