from django.urls import path 
from .views import * 

urlpatterns = [
    path('warehouses/', warehouses, name='warehouses'),
    path('areas/', areas, name='areas'),
    path('regions/', regions, name='regions'), 
    path('settlements/', settlements, name='settlements'), 
]

