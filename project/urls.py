from django.urls import path 
from .views import * 

static_urls = [
  # urls for static pages  
  path("",          index,    name='index'),
  path('services/', services, name="services"),
  path("about/",    about,    name='about'),
  path('contacts/', contacts, name="contacts"),
  path('profile/',  profile,  name='profile'),
  path("thank_you/",thank_you,name='thank_you'),
  path('basket/',   basket,   name='basket'),
  path("search/",   search,   name='search'),
  path("blog/",     blog,     name='blog'),
]
dynamic_urls = [
  # urls with slugs(post, product, category, etc)
  path("post_category/<slug>/",post_category, name='post_category'),
  path("item_category/<slug>/",item_category, name='item_category'),
  path("item/<slug>/",         item,          name='item'),
  path("post/<slug>/",         post,          name='post'),
]
urlpatterns = []
urlpatterns.append(static_urls)
urlpatterns.append(dynamic_urls)

