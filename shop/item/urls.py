from django.urls import path 
from .views import * 


urlpatterns = [
  path('feed_items/', feed_items, name="feed_items"),
  path('export_item_photoes/<slug>/', export_item_photoes, name='export_item_photoes'),
  path('export_item/<slug>/', export_item, name='export_item'),
]
