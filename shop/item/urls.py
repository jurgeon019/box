from django.urls import path 
from .views import * 


urlpatterns = [
  path('feed_items/', feed_items, name="feed_items"),
]
