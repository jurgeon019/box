from shop.cart.models import Cart, CartItem
from shop.cart.api.serializers import CartItemSerializer
from django.db.models import Sum


def get_cart(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id, ordered=False)
	except Exception as e:
		print(e)
		cart = Cart()
		cart.save()
		request.session['cart_id'] = cart.id
		cart = Cart.objects.get(id=cart.id, ordered=False)
	return cart


def get_cart_info(request):

  cart_items = CartItem.objects.filter(cart=get_cart(request))

  #TODO: зробити сумування не пітонячим циклом, а якось пройтись SQLьом
  #TODO 2: не получиться, бо total_price зроблено через @property, а має бути окремим полем

  cart_total_price = 0
  for cart_item in cart_items:
    cart_total_price += int(cart_item.total_price)

  cart_items_quantity = 0
  for cart_item in cart_items:
    cart_items_quantity += cart_item.quantity

  cart_items_count = cart_items.count()

  return {
    'cart_items':CartItemSerializer(cart_items, many=True).data,
    "cart_total_price":cart_total_price,
    "cart_items_count":cart_items_count,
    "cart_items_quantity":cart_items_quantity,
  }


