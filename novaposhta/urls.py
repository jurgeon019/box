
from django.urls import path

from .views import *

# app_name = 'novaposhta'


urlpatterns = [
    path('np/<action>/<content>/<type>/', np, name='np'),
]


