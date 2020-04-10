import requests
from django.http import HttpResponse, JsonResponse 


def gen_url(params, method):
  delivery_url = 'https://www.delivery-auto.com/api/v4/Public/'
  query = '?'
  for k,v in params.items():
    query += f'{k}={v}&'
  query = query[:-1]
  query = f'{delivery_url}{method}{query}'
  return query


def regions_list(request):  # області
  params    = {
    "culture": request.GET.get('culture', 'uk-UA'), # 'uk-UA' | 'en-US' | 'ru-RU'
    "country": request.GET.get('country', 1) # 1 | 2
  }
  return JsonResponse(requests.get(gen_url(params, "GetRegionList")).json())


def areas_list(request): # міста
  params   = {
    "culture" : request.GET.get('culture', 'uk-UA'), # 'uk-UA' | 'en-US' | 'ru-RU'
    "country" : request.GET.get('country', 1), # 1 | 2
    "regionId": request.GET.get('regionId', 3898),  # 3898 - 3921
    "fl_all"  : request.GET.get('fl_all'),  # True | False 
  } 
  return JsonResponse(requests.get(gen_url(params, "GetAreasList")).json())

 
def warehouses_list(request): # відділення
  params = {
    'culture':request.GET.get('culture', 'uk-UA'),  # 'uk-UA' | 'en-US' | 'ru-RU'
    "country":request.GET.get('country', 1),  # 1 | 2
    "includeRegionalCenters":request.GET.get("includeRegionalCenters"),
    "CityId":request.GET.get('CityId'),
    "RegionId":request.GET.get('RegionId'),
  }
  return JsonResponse(requests.get(gen_url(params, "GetWarehousesList")).json())




