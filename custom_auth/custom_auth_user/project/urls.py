from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usermodel.views')),
    path('auth/', include('userauth.views')),
]
