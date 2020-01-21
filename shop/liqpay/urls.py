from django.urls import path 
from .views import * 


urlpatterns = [
  path("payment/",      payment,      name='payment'),
  path("pay_callback/", pay_callback, name='pay_callback'),
]
