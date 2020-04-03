from django.urls import path, include 
from .views import * 


urlpatterns = [
    path('', include('box.sw_auth.api.urls')),
    path('sw_logout/', sw_logout, name='sw_logout')
]
