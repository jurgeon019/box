from box.apps.sw_shop.sw_order.models import ( Order, ItemRequest )
from box.apps.sw_shop.sw_catalog.models import Item 
from box.apps.sw_shop.sw_cart.utils import get_cart
from box.apps.sw_shop.sw_cart.models import Cart, CartItem
from box.core.mail import box_send_mail 
from box.core.sw_global_config.models import *

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.conf import settings 

from rest_framework.viewsets import ModelViewSet
from .serializers import *

class OrderViewSet(ModelViewSet):
  serializer_class = OrderSerializer 
  queryset = Order.objects.all()




from django.utils.translation import gettext_lazy as _







@csrf_exempt
def order_items(request):
  query        = request.POST or request.GET
  print(query)
  # import pdb; pdb.set_trace()
  name         = query.get('name', "---")
  email        = query.get('email', "---")
  phone        = query.get('phone', "---")
  address      = query.get('address', "---")
  comments     = query.get('comments', "---")

  payment_opt  = query.get('payment', "---")
  delivery_opt = query.get('delivery_opt', "---")

  order        = Order.objects.create(
    name         = name,
    email        = email,
    phone        = phone,
    address      = address,
    comments     = comments,
    payment_opt  = payment_opt,
    delivery_opt = delivery_opt,
  )
  cart        = get_cart(request)
  cart.order  = order
  cart.save()
  if payment_opt == 'liqpay':
    order.payment_opt = _("З передоплатою")
    order.save()
    url = reverse('payment')
    return JsonResponse({"url":url})
  else:
    order.payment_opt = _("Без предоплати")
    order.make_order(request)
    url = reverse('thank_you')
    return JsonResponse({"url":url})



@csrf_exempt
def order_request(request):
    print(request.POST)
    name    = request.POST.get('name', '---')
    email   = request.POST.get('email', '---')
    phone   = request.POST.get('phone', '---')
    address = request.POST.get('address', '---')
    item_id = request.POST.get('product_id', '---')
    payment = 'Покупка в 1 клік(при покупці в 1 клік оплати немає)'

    cart = get_cart(request)
    
    cart_item = CartItem.objects.create(
      cart=cart,
    )
    cart_item.item = Item.objects.get(id=item_id)
    cart_item.save()
    cart.items.add(cart_item)

    order = Order.objects.create(
      name    = name,    
      email   = email,   
      phone   = phone,   
      address = address,
      payment_opt = payment,
    )
    order.cart = cart
    order.save()
    order.make_order(request)
    return JsonResponse({
      'status':'OK',
      'url':reverse('thank_you'),
    })
  




@csrf_exempt
def item_info(request):
  query   = request.GET or request.POST
  item_id = query.get('product_id')
  name    = query.get('name', '---') 
  phone   = query.get('phone', '---') 
  email   = query.get('email', '---')
  message = query.get('message', '---') 
  item_request   = ItemRequest.objects.create(
    name=name,
    phone=phone,
    email=email,
    message=message,
  )
  if item_id:
    item = Item.objects.get(id=item_id)
    item_request.item = item
    item_request.save()

  box_send_mail(
    model=item_request, 
    subject=('Було отримано заявку на інформацію про товар'),
    recipient_list=NotificationConfig.objects.get_solo().get_data('other')['emails'],
  )
  return JsonResponse({
    'status':'OK',
  })


