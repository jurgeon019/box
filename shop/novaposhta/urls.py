
from django.urls import path

from box.shop.novaposhta import views


# app_name = 'novaposhta'


urlpatterns = [

    path('autocomplete/', views.autocomplete, name='autocomplete'),

    path('refresh/', views.refresh, name='refresh')

]


