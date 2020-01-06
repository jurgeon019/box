from django import template
from shop.order.models import Order
from shop.cart.models import CartItem
from shop.cart.utils import get_cart


register = template.Library()


@register.filter
def cart_item_count(request):
  cart = get_cart(request)
  return cart.items.all().count()


