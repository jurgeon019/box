from django import template
from box.shop.order.models import Order
from box.shop.cart.models import CartItem
from box.shop.cart.utils import get_cart


register = template.Library()


@register.filter
def cart_item_count(request):
  cart = get_cart(request)
  return cart.items.all().count()


