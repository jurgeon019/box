
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

from box.shop.novaposhta.lib import search_warehouses, refresh_warehouses


@login_required
def refresh(request):
    refresh_warehouses()
    return HttpResponse('Warehouses were successfully refreshed')


def autocomplete(request):

    query = request.GET.get('query')
    limit = request.GET.get('limit')
    query = query.capitalize()
    suggestions = [w.full_name for w in search_warehouses(query)]

    return JsonResponse({
        'query': query,
        'suggestions': suggestions
    })


