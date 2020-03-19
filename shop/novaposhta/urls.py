
from django.urls import path

from box.shop.novaposhta import views


# app_name = 'novaposhta'


urlpatterns = [
    path('refresh/', views.refresh, name='refresh')

]


