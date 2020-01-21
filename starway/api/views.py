from django.http import HttpResponse, JsonResponse
from .serializers import * 
from django.shortcuts import reverse, redirect
from ..models import * 


def become_member(request):
    response  = redirect(request.META['HTTP_REFERER'])
    full_name = request.POST['full_name']
    email     = request.POST['email']
    phone     = request.POST['phone']
    message   = request.POST['message']
    form = MemberRequest.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        message=message,
    )
    if request.is_ajax():
        response = JsonResponse({
            'status':'OK',
            'message':'Форма була відправлена',
        })
    return response