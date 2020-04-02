from django.http import JsonResponse
from rest_framework import generics 
from rest_framework.response import Response
from rest_framework.pagination import BasePagination, LimitOffsetPagination, PageNumberPagination, CursorPagination

from .serializers import *



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


class RegionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RegionSerializer 
    queryset = Region.objects.all() 



class SettlementsList(generics.ListCreateAPIView):
    serializer_class = SettlementSerializer 
    queryset = Settlement.objects.all() 
    pagination_class = StandardPageNumberPagination


class SettlementDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SettlementSerializer 
    queryset = Settlement.objects.all() 






def warehouses(request):
    query = request.GET.get('query')
    limit = request.GET.get('limit')
    if not query:
        return []
    query = query.capitalize()
    queryset = model_search(
        query, Warehouse.objects.all(), ['address', ],
    )
    if limit is not None:
        queryset =  queryset[:limit]
    warehouses = [warehouse.full_name for warehouse in queryset]
    return JsonResponse({
        'query': query,
        'warehouses': warehouses
    })


def areas(request):
    areas = Area.objects.all()
    areas = AreaSerializer(areas, many=True)
    return JsonResponse({
        'areas':areas.data
    })


def regions(request):
    query   = request.POST or request.GET
    area_id = query.get('area_id') 
    regions = Region.objects.all()
    if area_id:
        regions = regions.filter(area__id=area_id)
    regions = RegionSerializer(regions, many=True)
    return JsonResponse({
        'regions':regions.data
    })

def settlements(request):
    query       = request.POST or request.GET 
    region_id   = query.get('region_id')
    settlements = Settlement.objects.all()
    if region_id:
        settlements = settlements.filter(region__id=region_id)
    settlements = SettlementSerializer(settlements, many=True)
    return JsonResponse({
        'settlements':settlements.data
    })



