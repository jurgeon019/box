from django.urls import path, include 


urlpatterns = [
  path('', include('box.apps.sw_admin.api.urls')),
]
