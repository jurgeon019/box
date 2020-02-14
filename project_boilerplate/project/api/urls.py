from django.urls import path 
from .views import * 

urlpatterns = [
    path('contact_form/', contact_form, name='contact_form'),
]
