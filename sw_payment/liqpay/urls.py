from django.urls import path, include 



urlpatterns = [
  path('', include('box.sw_payment.liqpay.api.urls')),
    
]
