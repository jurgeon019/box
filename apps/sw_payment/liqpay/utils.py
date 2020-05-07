from django.shortcuts import redirect
from django.conf import settings 

from .models import LiqpayConfig
from .forms import LiqpayTransactionForm
from .liqpay import LiqPay


def get_liqpay_context(params): 
  config    = LiqpayConfig.get_solo()
  if config.sandbox_mode:
    public  = config.liqpay_sandbox_public_key
    private = config.liqpay_sandbox_private_key
  else:
    public  = config.liqpay_public_key
    private = config.liqpay_private_key
  liqpay    = LiqPay(public, private)
  return liqpay.cnb_signature(params), liqpay.cnb_data(params)  


def get_response(request):
  data      = request.POST.get('data')
  signature = request.POST.get('signature')
  config    = LiqpayConfig.get_solo()
  if config.sandbox_mode:
    public  = config.liqpay_sandbox_public_key
    private = config.liqpay_sandbox_private_key
  else:
    public  = config.liqpay_public_key
    private = config.liqpay_private_key
  liqpay    = LiqPay(public, private)
  sign      = liqpay.str_to_sign(private + data + private)
  response  = liqpay.decode_data_from_str(data)
  if sign == signature: print('callback is valid')
  return response


def create_liqpay_transaction(request):
  response = get_response(request)
  status   = response.get('status', '')
  if status == 'failure':
    return redirect('/')
  form    = LiqpayTransactionForm(response)
  if form.is_valid():
    form.save()
    return form






