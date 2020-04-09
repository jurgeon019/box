from django.urls import path 
from .views import * 


urlpatterns = [
    path('get_apps_list/', get_apps_list, name='get_apps_list'),
]



