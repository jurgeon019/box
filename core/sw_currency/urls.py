from django.urls import path, include 
from django.http import JsonResponse
import requests 
from .views import * 


urlpatterns = [
    path('api/currencies/', currencies, name='currencies'),
    path('api/create_currencies/', create_currencies, name='create_currencies'),
]


