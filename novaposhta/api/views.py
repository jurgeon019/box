
from ..lib import search_warehouses
from ..settings import NOVA_POSHTA_API_KEY
from django.http import JsonResponse
import requests 

def autocomplete(request):
    query = request.GET.get('query')
    limit = request.GET.get('limit')
    query = query.capitalize()
    suggestions = [w.full_name for w in search_warehouses(query)]
    return JsonResponse({
        'query': query,
        'suggestions': suggestions
    })



def get_areas(request):
    response = {}
    return JsonResponse(response )



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



def create_settlements(response):
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
