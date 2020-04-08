from django.urls import path, include 
from .views import * 

from rest_framework.routers import DefaultRouter 


router = DefaultRouter()
router.register('users', UserViewSet)

api_urls = [
    path('current_user/',    current_user),
    path('users/login/',     sw_login),
    # backward compatibility
    path('custom_login/',    sw_login, name='custom_login'),
    path('custom_logout/',   sw_logout, name='custom_logout'),
    path('custom_register/', sw_register, name='custom_register'),

]



urlpatterns = [
    path('', include(api_urls)),
    path('api/', include(router.urls)),
    path('api/', include(api_urls)),
]
