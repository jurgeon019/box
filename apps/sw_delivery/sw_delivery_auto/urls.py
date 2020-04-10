from django.urls import path, include 
from .views import * 


urlpatterns = [
    path('api/', include('box.apps.sw_delivery.sw_delivery_auto.api.urls')),  
    path('da/regions_list/', regions_list, name='regions_list'),  
    path('da/areas_list/', areas_list, name='areas_list'),  
    path('da/warehouses_list/', warehouses_list, name='warehouses_list'),  
]
