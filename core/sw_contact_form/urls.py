from django.urls import path, include 

urlpatterns = [
  path('', include('box.core.sw_contact_form.api.urls')),
]
