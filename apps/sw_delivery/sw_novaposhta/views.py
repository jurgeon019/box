
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

from .utils import *




@login_required
def np(request, action='refresh', content='warehouses', type='from_api'):
    '''
    :action: refresh | browse 
    :content: warehouses | settlements 
    :type: from_json | gen_json | from_api 


    ?limit=150&pages_limit=5&page=3

    /np/browse/settlements/
    /np/browse/warehouses/

    /np/refresh/settlements/gen_json/
    /np/refresh/warehouses/gen_json/
    /np/refresh/settlements/from_json/
    /np/refresh/warehouses/from_json/

    /np/refresh/settlements/from_api/
    /np/refresh/warehouses/from_api/
    '''
    query    = request.POST or request.GET 
    response = handle_np(query, action, content, type)
    return response

