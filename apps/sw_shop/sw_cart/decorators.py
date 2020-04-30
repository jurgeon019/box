from functools import wraps
from django.shortcuts import redirect
from box.apps.sw_shop.sw_cart.utils import get_cart
from box.apps.sw_shop.sw_order.models import Order, CartItem


def cart_exists(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
    cart   = get_cart(request)
    if not CartItem.objects.filter(cart=cart).exists():
        print('cart_items do not exists')
        return redirect('/')
    # if not Order.objects.filter(cart=cart).exists():
    # # if not Order.objects.filter(cart=cart,ordered=False).exists():
    #     print('order does not exist')
    #     return redirect('/')
    return function(request, *args, **kwargs)
  return wrap



