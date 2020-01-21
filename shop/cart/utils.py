from box.shop.cart.models import Cart, CartItem
from box.shop.cart.api.serializers import CartItemSerializer
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
  cart = get_cart(request)
  cart_items = CartItem.objects.filter(cart=cart)
  print(cart.currency)
  return {
    'cart_items':CartItemSerializer(cart_items, many=True).data,
    "cart_total_price":cart.total_price,
    "cart_items_count":cart.items_count,
    "cart_items_quantity":cart.items_quantity,
	"cart_currency":cart.currency,
  }

