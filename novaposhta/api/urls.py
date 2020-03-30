from django.urls import path 
from .views import * 

urlpatterns = [
    path('autocomplete/', autocomplete, name='autocomplete'),
    path('get_areas/', get_areas, name='get_areas'),
]
