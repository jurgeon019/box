from .models import Order 
from box.apps.sw_shop.sw_cart.utils import get_cart
from box.apps.sw_shop.sw_cart.models import CartItem
from box.apps.sw_payment.liqpay.utils import get_liqpay_context
from box.apps.sw_payment.liqpay.models import LiqpayConfig


def get_order_liqpay_context(request, params={}):
  cart  = get_cart(request)
  order = Order.objects.get(
    cart=cart,
    ordered=False,
  )
  amount = 0 
  for cart_item in CartItem.objects.filter(cart=cart):
    amount += cart_item.total_price
  def_params = {
    'amount': amount,
    'description': str(order.comments),
    'order_id': str(order.id),
    'action': 'pay',
    'currency': 'UAH',
    'version': '3',
    'sandbox': int(LiqpayConfig.get_solo().sandbox_mode), 
    'server_url': f'/sw_order/liqpay_callback/', 
    # 'server_url': f'{Site.objects.get_current()}pay_callback/', 
  }
  def_params.update(params)
  signature, data = get_liqpay_context(def_params)
  context = {
    'signature': signature,
    'data': data,
    'callback_url':'/sw_order/liqpay_callback/',
  }
  return context 
