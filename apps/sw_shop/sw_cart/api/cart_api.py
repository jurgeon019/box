from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from box.apps.sw_shop.sw_catalog.models import Item
from box.apps.sw_shop.sw_cart.models import CartItem
from box.apps.sw_shop.sw_cart.utils import get_cart, get_cart_info



@csrf_exempt
def get_cart_items(request):
  return JsonResponse(get_cart_info(request))


@csrf_exempt
def add_cart_item(request):
  cart = get_cart(request)
  query = request.POST or request.GET
  quantity = query.get('quantity', 1)
  item_id  = query['item_id']
  cart.add_item(item_id, quantity)
  return JsonResponse(get_cart_info(request))


@csrf_exempt
def remove_cart_item(request):
  cart = get_cart(request)
  query = request.POST or request.GET
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
  cart = get_cart(request)
  query = request.POST or request.GET
  item_id   = query['item_id']
  quantity  = query['quantity']
  cart_item = cart.change_item_amount(item_id, quantity)
  response  = {
    "cart_item_id":cart_item.id,
  }
  response.update(get_cart_info(request))
  return JsonResponse(response)

