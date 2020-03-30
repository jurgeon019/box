
from django.urls import path

from . import views


# app_name = 'novaposhta'


urlpatterns = [
    path('refresh/', views.refresh, name='refresh')

]


