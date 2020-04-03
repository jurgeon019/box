from django.urls import path, include 



urlpatterns = [
  path('', include('box.payment.liqpay.api.urls')),
    
]
