from django.urls import path, include 
from .views import * 

urlpatterns = [
    # path('warehouses/',  warehouses, name='warehouses'),
    # path('areas/',       areas, name='areas'),
    # path('regions/',     regions, name='regions'), 
    # path('settlements/', settlements, name='settlements'), 

    path('warehouses/',        WarehousesList.as_view()),
    path('warehouses/<pk>/',   WarehouseDetail.as_view()),
    path('regions/',           RegionsList.as_view()),
    path('regions/<pk>/',      RegionDetail.as_view()),
    path('settlements/<pk>/',  SettlementDetail.as_view()),
    path('settlements/',       SettlementsList.as_view()),
    path('areas/',             AreasList.as_view()),
    path('areas/<pk>/',        AreaDetail.as_view()),
]

