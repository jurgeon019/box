from django.urls import path 
from .views import * 


urlpatterns = [
    path('sw_view/', sw_view, name='sw_logout')
]
