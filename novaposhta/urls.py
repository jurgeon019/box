from django.urls import path, include 
from .views import *


urlpatterns = [
    path('api/', include('box.novaposhta.api.urls')),
    path('', include('box.novaposhta.api.urls')),
    path('np/<action>/<content>/<type>/', np, name='np'),
]


