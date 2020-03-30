
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
    return JsonResponse(response)


