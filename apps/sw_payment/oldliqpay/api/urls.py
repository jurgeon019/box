from django.urls import path 
from .views import pay_callback


urlpatterns = [
  path("pay_callback/", pay_callback, name='pay_callback'),
]
