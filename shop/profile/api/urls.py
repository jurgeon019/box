from django.urls import path 
from .views import * 


urlpatterns = [
    path('delete_order/<pk>/', delete_order,   name='delete_order'),
    path('update_profile/',    update_profile, name='update_profile'),
    path('get_orders/',    get_orders, name='get_orders'),
]
