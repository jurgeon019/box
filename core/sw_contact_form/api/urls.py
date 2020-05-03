from django.urls import path 
from .views import * 


urlpatterns = [
    path('sw_contact/', sw_contact, name='sw_contact'),
]
