from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, redirect
from shop.cart.utils import get_cart
from shop.order.forms import OrderForm
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from shop.order.models import Order 




def order_items(request):
  name         = request.POST.get('name')
  email        = request.POST.get('email')
  phone        = request.POST.get('phone')
  address      = request.POST.get('address')
  comments     = request.POST.get('comments')
  payment_opt  = request.POST.get('payment')
  delivery_opt = request.POST.get('delivery_opt')
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
  order.cart  = cart
  order.save()
  if payment_opt == 'liqpay':
    print(reverse(payment))
    url = reverse('payment')
    if request.is_ajax():
      return JsonResponse({"url":url})
    return redirect("payment")
  # elif payment_opt == 'manager':
  else:
    order.make_order(request)
    print(reverse('thank_you'))
    url = reverse('thank_you')
    return JsonResponse({"url":url})
    # return redirect('thank_you')
