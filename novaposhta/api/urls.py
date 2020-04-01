from django.urls import path 
from .views import * 

urlpatterns = [
    path('api/warehouses/', warehouses, name='warehouses'),
    path('api/areas/', areas, name='areas'),
    path('api/regions/', regions, name='regions'), 
    path('api/settlements/', settlements, name='settlements'), 
]

