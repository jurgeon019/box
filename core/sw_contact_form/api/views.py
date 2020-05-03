from .serializers import * 
from django.shortcuts import redirect 
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings 
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from ..models import *
from box.core.mail import box_send_mail
from box.core.sw_global_config.models import GlobalConfig


@csrf_exempt
def sw_contact(request):
    query    = request.POST or request.GET
    print(query)
    name     = query.get('name',    '---')
    email    = query.get('email',   '---')
    phone    = query.get('phone',   '---')
    message  = query.get('message', '---')
    url      = request.META.get('HTTP_REFERER')
    model    = Contact.objects.create(
        name=name,
        email=email,
        phone=phone,
        message=message,
        url=url
    )
    box_send_mail(
        subject=GlobalConfig.get_solo().get_data('contact')['subject'],
        recipients_list=GlobalConfig.get_solo().get_data('contact')['emails'],
        model=model,
    )
    return JsonResponse({
        'status':'OK',
        # 'url':'/'
        # 'redirect':reverse('index'),
    })







