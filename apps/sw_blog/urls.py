from django.urls import path, include 
from .views import * 


urlpatterns = [
  path('', include('box.apps.sw_blog.api.urls')),
]
