
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

from box.shop.novaposhta.lib import refresh_warehouses


@login_required
def refresh(request):
    refresh_warehouses()
    return HttpResponse('Warehouses were successfully refreshed')

