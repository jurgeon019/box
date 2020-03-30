import requests

from django.apps import apps
from django.conf import settings

from box.model_search import model_search

from .settings import NOVA_POSHTA_API_KEY
from .models import Warehouse


def search_warehouses(query, limit=None):

    if not query:
        return []

    queryset = model_search(
        # query, Warehouse.objects.all(), ['title', 'address'])
        query, Warehouse.objects.all(), ['address'])
        # query, Warehouse.objects.all(), ['title'])

    if limit is not None:
        return queryset[:limit]

    return queryset


def search_settlements(query, limit=None):
    if not query:
        return []
    
    queryset = model_search(

    )   



def refresh_warehouses():
    api_domain = 'https://api.novaposhta.ua'
    api_path = '/v2.0/json/AddressGeneral/getWarehouses'
    api_data = {
        'modelName': 'AddressGeneral',
        'calledMethod': 'getWarehouses',
        'apiKey': NOVA_POSHTA_API_KEY
    }
    response = requests.post(api_domain + api_path, json=api_data).json()
    if not response.get('success'):
        raise Exception(','.join(response.get('errors')))
    Warehouse.objects.all().delete()
    warehouses = []
    for item in response.get('data'):
        params = {
            'title': item.get('Description'),
            'address': item.get('CityDescription')
        }
        if apps.is_installed('modeltranslation'):
            langs = dict(settings.LANGUAGES)
            if 'uk' in langs:
                params.update({
                    'title_uk': item.get('Description'),
                    'address_uk': item.get('CityDescription')
                })
            if 'ru' in langs:
                params.update({
                    'title_ru': item.get('DescriptionRu'),
                    'address_ru': item.get('CityDescriptionRu')
                })
        warehouses.append(Warehouse(**params))
    Warehouse.objects.bulk_create(warehouses)



def settlements(request):

    api_domain = 'https://api.novaposhta.ua'

    api_path = '/v2.0/json/Address/searchSettlements'
    # api_path = '/v2.0/json/AddressGeneral/getSettlements'
    
    api_data = {
        'modelName': 'Address',
        'calledMethod': 'searchSettlements',
        # 'modelName': 'AddressGeneral',
        # 'calledMethod': 'getSettlements',
        'apiKey': NOVA_POSHTA_API_KEY,
        "methodProperties": {
        #     "CityName": "київ",
            "Limit": 5000,
            # "Page":"10",
        },
    }
    response = requests.post(api_domain + api_path, json=api_data).json()

    if not response.get('success'):
        raise Exception(','.join(response.get('errors')))

    # create_settlements(response)
    return JsonResponse(response)


def refresh_settlements(request):
    
    return JsonResponse(response)
