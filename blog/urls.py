from django.urls import path, include 



urlpatterns = [
  path('', include('box.blog.api.urls')),
]
