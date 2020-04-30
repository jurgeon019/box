
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from box.core.utils import get_user
from box.apps.sw_shop.sw_catalog.models import *
from box.apps.sw_shop.sw_cart.utils import get_cart

from .serializers import *


# FAVOURS
@csrf_exempt
def add_favour(request):
  '''
  '''
  query           = request.POST or request.GET
  item_id         = query['item_id']
  favour, created = FavourItem.objects.get_or_create(
    cart=get_cart(request),
    item=Item.objects.get(pk=int(item_id))
  )
  return HttpResponse()




@csrf_exempt
def remove_favour(request):
  '''
  Removes item from favours by clicking on trach bucket button on favours page 
  :favour_id: favour id
  '''
  query = request.POST or request.GET
  favour_id = query['favour_id']
  favour_item = FavourItem.objects.get(
    cart=get_cart(request),
    id=favour_id,
  )
  item_id = favour_item.item.id
  favour_item.delete()
  return HttpResponse(item_id)

@csrf_exempt
def remove_favour_by_like(request):
  '''
  Removes item from favours by clicking on heart-button on item card 
  :item_id: item id
  '''
  query   = request.POST or request.GET
  item_id = query['item_id']
  FavourItem.objects.get(
    cart=get_cart(request), 
    item=Item.objects.get(pk=int(item_id))
  ).delete()
  return HttpResponse()


@csrf_exempt
def add_favour_to_cart(request):
  query        = request.POST or request.GET
  item_id      = query['item_id']
  favour_id    = query['favour_id']
  cart_item, _ = CartItem.objects.get_or_create(
    cart=get_cart(request),
    item=Item.objects.get(id=item_id),
    ordered=False,
  )
  quantity = 1
  if _: cart_item.quantity = int(quantity)
  if not _: cart_item.quantity += int(quantity)
  cart_item.save()
  favouritem = FavourItem.objects.get(id=favour_id)
  favouritem.delete()
  return HttpResponse('ok')


@csrf_exempt
def add_favours_to_cart(request):
  favours = FavourItem.objects.filter(cart=get_cart(request))
  for favour in favours:
    cart_item, created = CartItem.objects.get_or_create(
      cart=get_cart(request),
      item=Item.objects.get(id=favour.item.id),
      ordered=False,
    )
    quantity = 1
    if created: cart_item.quantity = int(quantity)
    if not created: cart_item.quantity += int(quantity)
    cart_item.save()
    favour.delete()
  return HttpResponse('ok')


@csrf_exempt
def get_favours_amount(request):
  favours = FavourItem.objects.filter(cart=get_cart(request))
  return HttpResponse(favours.count())


@csrf_exempt
def get_favours(request):
  favours = FavourItem.objects.filter(
    cart=get_cart(request),
  )
  serializer = FavourItemSerializer(favours, many=True)
  response = {
    'favours':serializer.data, 
  }
  return JsonResponse(response)

