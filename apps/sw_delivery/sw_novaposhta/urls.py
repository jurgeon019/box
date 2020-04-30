from django.urls import path, include 
from .views import *


def sdfsdf(request):
    return HttpResponse()

urlpatterns = [
    path('babalsdfsdf/', sdfsdf, name='sdfsdf'),
    path('api/', include('box.apps.sw_delivery.sw_novaposhta.api.urls')),
    path('np/<action>/<content>/<type>/', np, name='np'),
]


