from django.urls import path 
from .views import * 

urlpatterns = [
    path('api/become_member/', become_member)
]
