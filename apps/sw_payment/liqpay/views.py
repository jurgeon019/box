from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect 


@csrf_exempt
def pay_callback(request):
  create_liqpay_transaction(request)
  return redirect('thank_you')


