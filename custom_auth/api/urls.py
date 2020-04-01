from django.urls import path, include 
from .views import * 


api_urls = [
    path('custom_login/', custom_login, name="custom_login"),
    path('custom_logout/', custom_logout, name="custom_logout"),
    path('custom_register/', custom_register, name="custom_register"),

    path('user_status/', user_status, name='user_status'),
]



urlpatterns = [
    path('', include(api_urls)),
    path('api/', include(api_urls)),
]
