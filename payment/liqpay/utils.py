from django.shortcuts import redirect
from django.conf import settings 

from box.global_config.models import SiteConfig
from box.sw_shop.order.models import Order
from box.sw_shop.cart.utils import get_cart
from box.sw_shop.cart.models import CartItem
from .forms import PaymentForm
from .liqpay import LiqPay



def get_liqpay_context(request):
  config = SiteConfig.get_solo()

  cart   = get_cart(request)
  order  = Order.objects.get(
    cart=cart,
    ordered=False,
  )
  order_id = order.id
  total_price = 0
  for cart_item in CartItem.objects.filter(ordered=False, cart=cart):
    total_price += cart_item.total_price
  
  params = {
      'action': 'pay',
      'amount': float(total_price),
      'currency': 'UAH',
      'description': str(order.comments),
      'order_id': str(order.id),
      'version': '3',
      'sandbox': 1, # sandbox mode, set to 1 to enable it
      'server_url': f'{site}pay_callback/', # url to callback view
  }
  liqpay    = LiqPay(config.liqpay_public_key, config.liqpay_private_key)
  signature = liqpay.cnb_signature(params)
  data      = liqpay.cnb_data(params)
  return signature, data  


def get_response(request):
  print(request.POST)
  print(request.POST)
  print(request.POST)
  print(request.POST)
  print(request.POST)
  print(request.POST)
  print("request.POST")
  config = SiteConfig.get_solo()
  liqpay    = LiqPay(config.liqpay_public_key, config.liqpay_private_key)
  data      = request.POST.get('data')
  signature = request.POST.get('signature')
  sign      = liqpay.str_to_sign(config.liqpay_private_key + data + config.liqpay_private_key)
  response  = liqpay.decode_data_from_str(data)
  print(response)
  if sign == signature: 
    print('callback is valid')
  return response



def create_payment(response, request):
  status   = response.get('status', '')
  order_id = response.get('order_id', '')
  print(status, order_id)
  order   = Order.objects.get(id=order_id)
  if status == 'failure':
    return redirect('/')
  form    = PaymentForm(response)
  payment = form.save(commit=False)
  payment.order = Order.objects.get(pk=order_id)
  payment.save()
  order.make_order(request)


