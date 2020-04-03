from django.urls import path, include 
from .views import * 

urlpatterns = [
    path('warehouses/',  warehouses, name='warehouses'),
    path('areas/',       areas, name='areas'),
    path('regions/',     regions, name='regions'), 
    path('settlements/', settlements, name='settlements'), 

    path('warehouses_list/',        WarehousesList.as_view()),
    path('areas_list/',             AreasList.as_view()),
    path('regions_list/',           RegionsList.as_view()),
    path('settlements_list/',       SettlementsList.as_view()),
    path('warehouse_detail/<pk>/',  WarehouseDetail.as_view()),
    path('area_detail/<pk>/',       AreaDetail.as_view()),
    path('region_detail/<pk>/',     RegionDetail.as_view()),
    path('settlement_detail/<pk>/', SettlementDetail.as_view()),
]

