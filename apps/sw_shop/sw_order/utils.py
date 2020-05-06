from .models import Payment, Order 


def create_payment(response)
  order    = Order.objects.get(id=response['order_id'])
  payment  = PaymentForm(response)
  payment  = form.save(commit=False)
  payment.order = Order.objects.get(pk=order_id)
  payment.save()
  order.make_order(request)


