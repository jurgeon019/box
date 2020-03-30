from django.http import JsonResponse

from ..settings import NOVA_POSHTA_API_KEY
from .serializers import *


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



