from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from box.apps.sw_shop.sw_catalog.models import Item
from box.apps.sw_shop.sw_cart.models import CartItem
from box.apps.sw_shop.sw_cart.utils import get_cart, get_cart_info
from rest_framework.decorators import api_view
from rest_framework.response import Response



@api_view(['GET','POST','DELETE'])
def cart_items(request):
  cart       = get_cart(request)
  if request.method == 'GET':
    return Response(data=get_cart_info(request),status=200)
  if request.method == 'POST':
    query      = request.data
    quantity   = query.get('quantity', 1)
    item_id    = query['item_id']
    attributes = query.get('attributes', [])
    cart.add_item(item_id, quantity, attributes)
    return Response(data=get_cart_info(request), status=200)
  if request.method == 'DELETE':
    cart.clear()
    return Response(data=get_cart_info(request), status=200)


@api_view(['GET','PATCH','DELETE'])
def cart_item(request, id):
  cart = get_cart(request)
  if request.method == 'GET':
    cart_item = CartItem.objects.get(id=id)
    return Response(data=CartItemSerializer(cart_item).data, status=200)
  elif request.method == 'PATCH':
    query        = request.data
    # cart_item_id = query['cart_item_id']
    cart_item_id = id
    quantity     = query['quantity']
    cart_item    = cart.change_cart_item_amount(cart_item_id, quantity)
    response     = {
      "cart_item_id":cart_item_id,
      "cart_item_total_price":cart_item.total_price,
    }
    response.update(get_cart_info(request))
    return Response(data=response, status=200)
  elif request.method == 'DELETE':
    cart         = get_cart(request)
    query        = request.POST or request.GET
    # cart_item_id = query['cart_item_id']
    cart_item_id = id
    cart.remove_cart_item(cart_item_id)
    return Response(get_cart_info(request), status=204)



@api_view(['GET','POST'])
def check_if_item_with_attributes_is_in_cart(request):
  return Response 




# old 

@csrf_exempt
def get_cart_items(request):
  return JsonResponse(get_cart_info(request))

import json 
@api_view(['GET','POST'])
def add_cart_item(request):
  # query      = request.data 
  query      = request.POST or request.GET
  cart       = get_cart(request)
  # print("query::",query)
  quantity   = query.get('quantity', 1)
  item_id    = query['item_id']
  attributes = json.loads(query.get('attributes', []))
  # print(attributes)
  cart.add_item(item_id, quantity, attributes)
  return JsonResponse(get_cart_info(request))


@csrf_exempt
def remove_cart_item(request):
  cart         = get_cart(request)
  query        = request.POST or request.GET
  cart_item_id = query['cart_item_id']
  cart.remove_cart_item(cart_item_id)
  return JsonResponse(get_cart_info(request))


@csrf_exempt
def clear_cart(request):
  cart = get_cart(request)
  cart.clear()
  return JsonResponse(get_cart_info(request))


@csrf_exempt
def change_cart_item_amount(request):
  query = request.POST or request.GET
  cart_item_id = query['cart_item_id']
  quantity     = query['quantity']
  cart         = get_cart(request)
  cart_item    = cart.change_cart_item_amount(cart_item_id, quantity)
  response     = {
    "cart_item_id":cart_item_id,
    "cart_item_total_price":cart_item.total_price,
  }
  response.update(get_cart_info(request))
  return JsonResponse(response)


@csrf_exempt
def change_item_amount(request):
  cart      = get_cart(request)
  query     = request.POST or request.GET
  item_id   = query['item_id']
  quantity  = query['quantity']
  cart_item = cart.change_item_amount(item_id, quantity)
  response  = {
    "cart_item_id":cart_item.id,
  }
  response.update(get_cart_info(request))
  return JsonResponse(response)

