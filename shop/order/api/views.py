from box.shop.order.models import ( Order, OrderRequest )
from box.shop.item.models import Item 
from box.shop.cart.utils import get_cart
from box.shop.cart.models import Cart, CartItem

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse




@csrf_exempt
def order_items(request):
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
    return JsonResponse({'status':'OK'})
  



