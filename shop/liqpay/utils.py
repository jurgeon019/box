from .liqpay import LiqPay
from box.shop.order.models import Order
from box.shop.cart.utils import get_cart
from django.shortcuts import redirect
from box.shop.cart.models import CartItem
from django.conf import settings 
from .forms import PaymentForm


def get_liqpay_context(request):
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
      'server_url': f'{settings.CURRENT_DOMEN}pay_callback/', # url to callback view
  }
  liqpay    = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
  signature = liqpay.cnb_signature(params)
  data      = liqpay.cnb_data(params)
  return signature, data  


def get_response(request):
  liqpay    = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
  data      = request.POST.get('data')
  signature = request.POST.get('signature')
  sign      = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
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


