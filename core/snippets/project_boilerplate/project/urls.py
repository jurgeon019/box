from django.urls import path, include 
from .views import * 


urlpatterns = [
    path('',                index,    name='index'),
    path('about/',          about,    name='about'),
    path('blog/',           blog,     name='blog'),
    path('post/<slug>/',    post,     name='post'),
    path('contacts/',       contacts, name='contacts'),
    path('catalog/<slug>/', catalog,  name='catalog'),
    path('item/<slug>/',    item,     name='item'),

]
