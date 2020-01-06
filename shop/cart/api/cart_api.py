from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from shop.item.models import Item
from shop.cart.models import CartItem
from shop.cart.utils import get_cart, get_cart_info



@csrf_exempt
def get_cart_items(request):
  return JsonResponse(get_cart_info(request))


@csrf_exempt
def add_cart_item(request):
  quantity = request.POST.get('quantity', 1)
  item_id  = request.POST['item_id']
  try: quantity = int(quantity)
  except: quantity = 1
  item = get_object_or_404(Item, pk=int(item_id))
  cart_item, created = CartItem.objects.get_or_create(
    cart=get_cart(request),
    item=item,
  )
  if created:
    cart_item.quantity = int(quantity)
  if not created:
    cart_item.quantity += int(quantity)
  cart_item.save()
  return JsonResponse(get_cart_info(request))


@csrf_exempt
def remove_cart_item(request):
  cart_item_id = request.POST['cart_item_id']
  cart_item = CartItem.objects.get(
    cart=get_cart(request),
    id=cart_item_id,
  )
  cart_item.delete()
  return JsonResponse(get_cart_info(request))


@csrf_exempt
def clear_cart(request):
  CartItem.objects.filter(
    cart=get_cart(request),
  ).delete()
  return JsonResponse(get_cart_info(request))


@csrf_exempt
def change_cart_item_amount(request):
  cart_item_id  = request.POST['cart_item_id']
  quantity      = request.POST['quantity']
  try: quantity = int(quantity)
  except: quantity = 1
  cart_item = CartItem.objects.get(id=cart_item_id, cart=get_cart(request))
  # cart_item = get_object_or_404(
  #   CartItem,
  #   id=cart_item_id,
  #   cart=get_cart(request),
  # )
  cart_item.quantity = quantity
  cart_item.save()

  response = {
    "cart_item_id":cart_item.id,
    "cart_item_total_price":cart_item.total_price,
  }
  response.update(get_cart_info(request))
  return JsonResponse(response)


@csrf_exempt
def change_item_amount(request):
  item_id       = request.POST['item_id']
  quantity      = request.POST['quantity']
  try: quantity = int(quantity)
  except: quantity = 1

  cart_item = get_object_or_404(
    CartItem,
    item__id=item_id,
    cart=get_cart(request),
  )
  cart_item.quantity = quantity
  cart_item.save()

  response = {
    "cart_item_id":cart_item.id,
    # "item_total_price":cart_item.total_price,
  }
  response.update(get_cart_info(request))
  return JsonResponse(response)
