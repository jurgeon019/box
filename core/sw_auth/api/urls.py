from django.urls import path, include 
from .views import * 

from rest_framework.routers import DefaultRouter 


router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('current_user_info/',    current_user_info),
    path('users/sw_login/',  sw_login),
    path('users/sw_logout/', sw_logout),
    path('babaski/', sw_login),
    path('', include(router.urls)),
]


