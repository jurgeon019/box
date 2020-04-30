from django.http import JsonResponse
from rest_framework import generics 
from rest_framework.response import Response
from rest_framework.pagination import BasePagination, LimitOffsetPagination, PageNumberPagination, CursorPagination

from .serializers import *

from box.core.sw_model_search.lib import model_search


class StandardPageNumberPagination(PageNumberPagination):
    page_size              = 100
    max_page_size          = 1000
    page_query_param       = 'page_number'
    page_size_query_param  = 'per_page'


class StandardLimitOffsetPagination(LimitOffsetPagination):
    default_limit      = 10
    max_limit          = 1000
    limit_query_param  = 'limit'
    offset_query_param = 'offset'


class StandardCursorPagination(CursorPagination):
    page_size = 10 
    cursor_query_param = 'cursor'
    ordering = '-id'



class WarehousesList(generics.ListCreateAPIView):
    serializer_class = WarehouseSerializer 
    queryset = Warehouse.objects.all() 
    pagination_class = StandardPageNumberPagination
    def get_queryset(self):
        queryset = super().get_queryset()
        data     = self.request.query_params
        query    = data['query']
        query    = query.capitalize()
        queryset = model_search(
            query, Warehouse.objects.all(), ['address', ],
        )
        return queryset


class WarehouseDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WarehouseSerializer 
    queryset = Warehouse.objects.all() 



class AreasList(generics.ListCreateAPIView):
    serializer_class = AreaSerializer 
    queryset = Area.objects.all() 
    pagination_class = StandardPageNumberPagination


class AreaDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AreaSerializer 
    queryset = Area.objects.all() 


class RegionsList(generics.ListCreateAPIView):
    serializer_class = RegionSerializer 
    queryset = Region.objects.all() 
    pagination_class = StandardPageNumberPagination
    def get_queryset(self):
        queryset = super().get_queryset()
        data     = self.request.query_params
        query    = data.get('area_id')
        if area_id:
            queryset = queryset.filter(area__id=area_id)
        return queryset


class RegionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RegionSerializer 
    queryset = Region.objects.all() 


class SettlementsList(generics.ListCreateAPIView):
    serializer_class = SettlementSerializer 
    queryset = Settlement.objects.all() 
    pagination_class = StandardPageNumberPagination
    def get_queryset(self):
        queryset = super().get_queryset()
        data     = self.request.query_params
        region_id    = data.get('region_id')
        if region_id:
            queryset = queryset.filter(region__id=region_id)
        return queryset

class SettlementDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SettlementSerializer 
    queryset = Settlement.objects.all() 



