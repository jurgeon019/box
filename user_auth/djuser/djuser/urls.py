from django.urls import path, include
from django.contrib import admin


from accounts.views import activate_user_view, home, register, login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.views')),
]
