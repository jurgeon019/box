
from django.urls import path 
from .views import * 



urlpatterns = [
    path('credit_request/', credit_request, name='credit_request'),
    path('contact_request/',contact_request,name="contact_request"),
    path('order_request/',  order_request,  name="order_request"),
]

