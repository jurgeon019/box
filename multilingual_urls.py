from django.urls import path, include 

urlpatterns = [
  path('accounts/', include('allauth.urls')),
  path('test/', include('box.shop.test_shop.urls')),
  path('', include('box.shop.item.urls')),
  path('', include('box.shop.order.urls')),
  path('', include('box.shop.liqpay.urls')),
#   path('', include('box.pages.urls')),

]

