from django.shortcuts import redirect
from django.conf import settings 

from box.core.sw_global_config.models import SiteConfig
from .forms import PaymentForm
from .liqpay import LiqPay



def get_liqpay_context(params): 
  config    = SiteConfig.get_solo()
  liqpay    = LiqPay(config.liqpay_public_key, config.liqpay_private_key)
  signature = liqpay.cnb_signature(params)
  data      = liqpay.cnb_data(params)
  return signature, data  


def get_response(request):
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
  # TODO: Забрати звідси все що звязано з магазином 
  from box.apps.sw_shop.sw_order.models import Order 
  # from box.apps.sw_payment. sw_shop.sw_order.models import Order 
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


