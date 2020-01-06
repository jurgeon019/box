from django.shortcuts import render
from django.http import JsonResponse
from forms.models import CreditRequest, ContactRequest, OrderRequest
from shop.item.models import Item 
from django.views.decorators.csrf import csrf_exempt


def credit_request(request):
    print(request.POST)
    name    = request.POST.get('name')
    phone   = request.POST.get('phone')
    email   = request.POST.get('email')
    id      = request.POST.get('product_id')
    item    = Item.objects.get(id=id)
    credit  = CreditRequest.objects.create(
        item    = item,
        name    = name,
        phone   = phone,
        email   = email,
    )
    return JsonResponse({'status':'OK'})


@csrf_exempt
def contact_request(request):
    # print(request.POST)
    name    = request.POST.get('name')
    phone   = request.POST.get('phone')
    email   = request.POST.get('email')
    message = request.POST.get('message')
    contact = ContactRequest.objects.create(
        name = name,
        phone = phone,
        email = email,
        message = message,
    )
    return JsonResponse({'status':'OK'})



 
@csrf_exempt
def order_request(request):
    # print(request.POST)
    name    = request.POST.get('name')
    phone   = request.POST.get('phone')
    email   = request.POST.get('email')
    message = request.POST.get('message')
    order = OrderRequest.objects.create(
        name = name,
        phone = phone,
        email = email,
        message = message,
    )
    return JsonResponse({'status':'OK'})



 