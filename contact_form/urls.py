from django.urls import path, include 

urlpatterns = [
  path('', include('box.contact_form.api.urls')),
]
