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
  # import pdb; pdb.set_trace()
  name         = query.get('name', "---")
  email        = query.get('email', "---")
  phone        = query.get('phone', "---")
  address      = query.get('address', "---")
  comments     = query.get('comments', "---")

  payment_opt  = query.get('payment_opt', "---")
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

from rest_framework.decorators import api_view


import json 


@api_view(['GET','POST'])
def order_request(request):
    # query    = request.POST or request.GET
    query = request.data
    
    name     = query.get('name', '---')
    email    = query.get('email', '---')
    phone    = query.get('phone', '---')
    address  = query.get('address', '---')
    comments = query.get('comments', '---')
    attributes = json.loads(query.get('attributes'))
    item_id  = query['product_id']
    payment  = _('Покупка в 1 клік')
    delivery = _('Покупка в 1 клік')
    print(query)
    cart = get_cart(request)
    cart.add_item(item_id=item_id, quantity=1, attributes=attributes)
    order = Order.objects.create(
      name    = name,    
      email   = email,   
      phone   = phone,   
      address = address,
      delivery_opt = delivery,
      payment_opt = payment,
      cart = cart,
    )
    order.make_order(request)
    return JsonResponse({
      'status':'OK',
      'url':reverse('thank_you'),
    })

from ..models import OrderRecipientEmail
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
    subject=('Було отримано заявку на інформацію про товар'),
    template = 'sw_order/item_info_mail.html',
    email_config = OrderRecipientEmail,
    model=item_request, 
    fail_silently=False,
  )
  return JsonResponse({
    'status':'OK',
  })




