
from .liqpay import LiqPay
from django.conf import settings 
from shop.order.models import Order
from django.views.decorators.csrf import csrf_exempt
from shop.cart.utils import get_cart
from django.shortcuts import redirect, render
from shop.cart.models import CartItem
from django.conf import settings 


def payment(request):
  cart   = get_cart(request)
  order  = Order.objects.filter(
    cart=cart,
    ordered=False,
  )
  cart_items = cart.items.all()
  if not cart_items.exists():
    return redirect('/')

  if not order.exists():
    return redirect('/')

  
  order = order.first()
  total_price = 0
  for cart_item in CartItem.objects.filter(ordered=False, cart=cart):
    total_price += cart_item.total_price

  params = {
      'action': 'pay',
      'amount': float(total_price),
      'currency': 'UAH',
      'description': str(order.comments),
      'order_id': str(order.id+1000),
      'version': '3',
      'sandbox': 1, # sandbox mode, set to 1 to enable it
      'server_url': f'{settings.CURRENT_DOMEN}pay_callback/', # url to callback view
  }
  liqpay    = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
  signature = liqpay.cnb_signature(params)
  data      = liqpay.cnb_data(params)
  return render(request, 'payment.html', {'signature': signature, 'data': data})


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


@csrf_exempt
def pay_callback(request):
  print('pay callback')
  response = get_response(request)
  create_payment(response)
  return redirect('thank_you')


def create_payment(response):
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




















# @csrf_exempt
# def pay_callback(request):
#     print('pay callback')
#     liqpay    = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
#     data      = request.POST.get('data')
#     signature = request.POST.get('signature')
#     sign      = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
#     response  = liqpay.decode_data_from_str(data)
#     if sign == signature: print('callback is valid')
#     print(response)

#     action              = response.get('action', '')
#     payment_id          = response.get('payment_id', '')
#     status              = response.get('status', '')
#     version             = response.get('version', '')
#     type                = response.get('type', '')
#     paytype             = response.get('paytype', '')
#     public_key          = response.get('public_key', '')
#     acq_id              = response.get('acq_id', '')
#     order_id            = response.get('order_id', '')
#     liqpay_order_id     = response.get('liqpay_order_id', '')
#     description         = response.get('description', '')
#     sender_phone        = response.get('sender_phone', '')
#     sender_first_name   = response.get('sender_first_name', '')
#     sender_last_name    = response.get('sender_last_name', '')
#     sender_card_mask2   = response.get('sender_card_mask2', '')
#     sender_card_bank    = response.get('sender_card_bank', '')
#     sender_card_type    = response.get('sender_card_type', '')
#     sender_card_country = response.get('sender_card_country', '')
#     ip                  = response.get('ip', '')
#     amount              = response.get('amount', '')
#     currency            = response.get('currency', '')
#     sender_commission   = response.get('sender_commission', '')
#     receiver_commission = response.get('receiver_commission', '')
#     agent_commission    = response.get('agent_commission', '')
#     amount_debit        = response.get('amount_debit', '')
#     amount_credit       = response.get('amount_credit', '')
#     commission_debit    = response.get('commission_debit', '')
#     commission_credit   = response.get('commission_credit', '')
#     currency_debit      = response.get('currency_debit', '')
#     currency_credit     = response.get('currency_credit', '')
#     sender_bonus        = response.get('sender_bonus', '')
#     amount_bonus        = response.get('amount_bonus', '')
#     mpi_eci             = response.get('mpi_eci', '')
#     is_3ds              = response.get('is_3ds', '')
#     language            = response.get('language', '')
#     create_date         = response.get('create_date', '')
#     end_date            = response.get('end_date', '')
#     transaction_id      = response.get('transaction_id', '')

#     if status == 'failure':
#       return redirect('thank_you')
#     order = Order.objects.get(id=order_id)
#     payment = Payment()
#     payment.status   = status
#     payment.status   = status
#     payment.ip       = ip
#     payment.amount   = amount
#     payment.currency = currency
#     payment.order    = Order.objects.get(pk=order_id)
#     payment.sender_phone        = sender_phone
#     payment.sender_first_name   = sender_first_name
#     payment.sender_last_name    = sender_last_name
#     payment.sender_card_mask2   = sender_card_mask2
#     payment.sender_card_bank    = sender_card_bank
#     payment.sender_card_type    = sender_card_type
#     payment.sender_card_country = sender_card_country
#     payment.save()
#     order.ordered=True
#     order.save()
#     send_order_mail()
#     return redirect('thank_you')


    