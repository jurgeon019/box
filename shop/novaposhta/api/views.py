
from box.shop.novaposhta.lib import search_warehouses
from django.http import JsonResponse


def autocomplete(request):
    query = request.GET.get('query')
    limit = request.GET.get('limit')
    query = query.capitalize()
    suggestions = [w.full_name for w in search_warehouses(query)]
    return JsonResponse({
        'query': query,
        'suggestions': suggestions
    })


