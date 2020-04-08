from django.urls import path 
from .views import * 



urlpatterns = [
  path('get_items/', get_items, name='get_items'),
  path('create_review/', create_review),
  
  path('get_item/', get_item, name='get_item'),

]





