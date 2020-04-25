from django.urls import path, include 

urlpatterns = [
  path('api/', include('box.core.sw_contact_form.api.urls')),
]
