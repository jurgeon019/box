from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages 
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .serializers import *

from box.apps.sw_shop.sw_order.models import OrderStatus, Order
from box.core.utils import get_user, get_sk

from rest_framework.viewsets import ModelViewSet









class CustomerGroupViewSet(ModelViewSet):
  serializer_class = CustomerGroupSerializer
  queryset = CustomerGroup.objects.all()


class CouponViewSet(ModelViewSet):
  serializer_class = CouponSerializer
  queryset = Coupon.objects.all()


class SubscriberViewSet(ModelViewSet):
  serializer_class = SubscriberSerializer
  queryset = Subscriber.objects.all()















# DEPRECATED. 

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
    'orders':OrderSerializer(orders, many=True).data,
  }
  return JsonResponse(response)

@csrf_exempt
def update_profile(request):
  first_name   = request.POST.get('first_name')
  last_name    = request.POST.get('last_name')
  phone_number = request.POST.get('phone_number')
  email        = request.POST.get('email')
  user              = request.user
  user.first_name   = first_name
  user.last_name    = last_name
  user.phone_number = phone_number
  user.email        = email
  user.save()
  messages.success(request, 'Ваші данні були оновлені')
  print(request.user)
  return JsonResponse({
    'status':'OK',
    'message':'Ваші данні були оновлені',
  })
  # return redirect('customer')


# @login_required
@csrf_exempt
def delete_order(request, pk):
  order = Order.objects.filter(
    pk=pk,
    user=get_user(request),
  )
  # order.delete()
  order.update(is_active=False)
  return redirect('customer')

