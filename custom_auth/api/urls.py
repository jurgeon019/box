from django.urls import path 
from .views import * 


urlpatterns = [
    path('custom_login/', custom_login),
    path('custom_logout/', custom_logout),
    path('custom_register/', custom_register),
]
