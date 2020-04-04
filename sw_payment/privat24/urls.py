from .views import *
from django.urls import path, include



urlpatterns = [
    path('pay_privat24/', pay_privat24, name='pay_privat24'),
    path('p24/', include(Privat24Integration().urls)),
]
