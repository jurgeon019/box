
from django.urls import path, include 
from .views import * 

urlpatterns = [
  path('', include('box.sw_payment.liqpay.api.urls')),
]
