import json 

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


def handle_np(query, action, content, type):
    limit       = query.get('limit', 150)
    page        = query.get('page', 1)
    pages_limit = query.get('pages_limit', None)
    if content == 'warehouses':
        method   = 'getWarehouses'
        model    = "AddressGeneral"
        message  = 'Warehouses were successfully refreshed'
        filename = 'warehouses.json'
        func     = create_warehouses
    elif content == 'settlements':
        method   = 'getSettlements'
        model    = "AddressGeneral"
        message  = 'Settlements were successfully refreshed'
        filename = 'settlements.json'
        func     = create_settlements
    if action == 'refresh':
        if type == 'gen_json':
            response = get_full_response(model, method,
                limit=limit,
                page=page,
                pages_limit=pages_limit,
            )
            with open(filename, 'w') as f:
                f.write(json.dumps(response, indent=4))
        elif type == 'from_api':
            response = get_full_response(model, method,
                limit=limit,
                page=page,
                pages_limit=pages_limit,
            )
            func(response)
        elif type == 'from_json':
            with open(filename, 'r') as f:
                func(json.load(f))
        return JsonResponse({
            "message":message,
            "status": "OK",
        })
    elif action == 'browse':
        response = get_response(model, method,
            limit=limit,
            page=page,
        )
        return JsonResponse(response)


