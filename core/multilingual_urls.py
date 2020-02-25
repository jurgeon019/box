from django.urls import path, include 

urlpatterns = [
  path('accounts/', include('allauth.urls')),
  path('', include('box.pages.urls')),
  path('', include('box.shop.item.urls')),
]

