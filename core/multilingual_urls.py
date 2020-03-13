from django.urls import path, include 

urlpatterns = [
  path('accounts/', include('allauth.urls')),
  path('', include('box.page.urls')),
  path('', include('box.shop.item.urls')),
]

