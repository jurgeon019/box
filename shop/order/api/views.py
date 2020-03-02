from box.shop.order.models import ( Order, OrderRequest, ItemRequest )
from box.shop.item.models import Item 
from box.shop.cart.utils import get_cart
from box.shop.cart.models import Cart, CartItem

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.core.mail import send_mail




@csrf_exempt
def order_items(request):
  print(request.POST)
  print(request.POST)
  print(request.POST)
  print(request.POST)
  print(request.POST)
  print(request.POST)
  print(request.POST)
  print(request.POST)
  print(request.POST)
  print(request.POST)
  print(request.POST)
  name         = request.POST.get('name', "---")
  email        = request.POST.get('email', "---")
  phone        = request.POST.get('phone', "---")
  address      = request.POST.get('address', "---")

  payment_opt  = request.POST.get('payment', "---")
  delivery_opt = request.POST.get('delivery_opt', "---")
  comments     = request.POST.get('comments', "---")

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
  print('CART 2', cart.id)
  print('ORDER 2', order.id)


  if payment_opt == 'liqpay':
    url = reverse('payment')
    return JsonResponse({"url":url})
  else:
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
  model   = ItemRequest.objects.create(
    name=name,
    phone=phone,
    email=email,
    message=message,
  )
  if item_id:
    item = Item.objects.get(id=item_id)
    model.item = item
    model.save()
  link  = reverse(f'admin:{model._meta.app_label}_{model._meta.model_name}_change', args=(model.id,))
  from django.conf import settings 
  send_mail(
    subject = 'Заявка на інформацію про товар',
    message = f'{settings.CURRENT_DOMEN+link}',
    from_email = settings.EMAIL_HOST_USER,
    recipient_list = [settings.EMAIL_HOST_USER,],
    fail_silently=False,
  )
  return JsonResponse({
    'status':'OK',
    
  })

