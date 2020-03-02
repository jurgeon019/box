from django.shortcuts import render, redirect, reverse
from box.core.utils import get_user, get_sk
from box.shop.order.models import Order
from django.shortcuts import get_object_or_404
from django.contrib import messages 
from django.utils.translation import gettext as _
from django.http import JsonResponse

from .serializers import OrderSerializer
from box.shop.order.models import Status 


@csrf_exempt
def get_orders(request):
  query     = request.GET or request.POST
  order_by  = query.get('order_by', '-created')
  status_id = query.get('status_id')
  orders    = Order.objects.filter(
    user=get_user(request),
  ).order_by(order_by)
  if status_id:
    orders = orders.filter(status__id=status_id)
  response = {
    'ДОПОМОГА ФРОНТЕНДЕРУ':{
      'order_by (поля заказів для сортування)':[
        'created',
        'name',
        'email',
        'phone',
        'address',
        '-created',
        '-name',
        '-email',
        '-phone',
        '-address',
      ],
      'status_id (статуси заказів для фільтрування)':list(Status.objects.all().values_list('id', flat=True)),
      'orders':OrderSerializer(orders, many=True).data,
    }
  }
  return JsonResponse(response)

@csrf_exempt
def update_profile(request):
  first_name   = request.POST['first_name']
  last_name    = request.POST['last_name']
  phone_number = request.POST['phone_number']
  email        = request.POST['email']
  user = request.user
  user.first_name=first_name
  user.last_name = last_name
  user.phone_number = phone_number
  user.email = email
  user.save()
  messages.success(request, 'Ваші данні були оновлені')
  print(request.user)
  return redirect('profile')


# @login_required
@csrf_exempt
def delete_order(request, pk):
  order = Order.objects.filter(
    pk=pk,
    user=get_user(request),
  )
  # order.delete()
  order.update(is_active=False)
  return redirect('profile')

