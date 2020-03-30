
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

from .lib import refresh_warehouses, refresh_settlements


@login_required
def refresh(request):
    refresh_warehouses()
    return HttpResponse('Warehouses were successfully refreshed')

@login_required
def refresh_settlements(request):
    refresh_settlements()
    return HttpResponse('Settlements were succesfully refreshed')