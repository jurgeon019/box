from shop.cart.models import *
from core.utils import get_sk, get_user
from shop.cart.utils import get_cart


 
def cart_content(request):
    cart         = get_cart(request)
    cart_items   = cart.items.all()
    favour_items = cart.favour_items.all()

    cart_items_amount = 0
    total_order_price = 0
    for cart_item in cart_items:
        cart_items_amount += cart_item.quantity
        total_order_price += cart_item.item.price * cart_item.quantity

    favour_items_amount = 0
    for favour_item in favour_items:
        favour_items_amount += 1
    request.session['total_price'] = total_order_price
    return locals()


