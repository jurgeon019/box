from django.urls import path, include 
from .views import * 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('items/', ItemViewSet)
router.register('reviews/', ReviewViewSet)

urlpatterns = [
  # path('', include(router.urls)),
  path('items/', ItemList.as_view()),
  path('items/<pk>/', ItemDetail.as_view()),
  # path('items/', ItemViewSet.as_view({'get':'list'})),
  # path('get_items/', get_items, name='get_items'),
  # path('create_review/', create_review),
  # path('get_item/', get_item, name='get_item'),
]





