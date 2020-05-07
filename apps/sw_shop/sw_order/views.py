

from django.shortcuts import render, redirect

from .models import Payment, Order 
from box.core.sw_currency.models import Currency
from box.apps.sw_payment.liqpay.utils import create_liqpay_transaction


def liqpay_callback(request):
  form          = create_liqpay_transaction(request)
  transaction   = form.instance
  order = Order.objects.get(id=transaction.order_id)
  payment       = Payment.objects.create(
    order=order,
    amount=transaction.amount,
    currency=Currency.objects.get(code=transaction.currency)
  )
  order.make_order(request)
  return redirect('thank_you')



