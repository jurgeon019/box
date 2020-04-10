from functools import wraps
from django.shortcuts import redirect
from box.apps.sw_shop.sw_cart.utils import get_cart
from box.apps.sw_shop.sw_order.models import Order


def cart_exists(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
    cart   = get_cart(request)
    order  = Order.objects.filter(
        cart=cart,
        # ordered=False,
    )

    print('CART  1', cart.id)
    print('ORDER 1', order)
    # return redirect(request.META['HTTP_REFERER'])
    cart_items = cart.items.all()
    if not cart_items.exists():
        print('cart_items do not exists')
        return redirect('/')
    if not order.exists():
        print('order does not exist')
        return redirect('/')
    return function(request, *args, **kwargs)
  return wrap



