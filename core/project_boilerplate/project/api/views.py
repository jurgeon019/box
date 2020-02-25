from .serializers import * 
from django.shortcuts import redirect 
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings 
from django.urls import reverse
from project.models import ContactForm


def contact_form(request):
    if request.method == 'GET':
        return JsonResponse({'sdf':'sdf'})
    query    = request.POST 
    name     = query.get('name', '')
    email    = query.get('email', '')
    phone    = query.get('phone', '')
    message  = query.get('message', '')
    model = ContactForm.objects.create(
        name=name,
        email=email,
        phone=phone,
        message=message,
    )
    link  = reverse(f'admin:{model._meta.app_label}_{model._meta.model_name}_change', args=(model.id,))
    send_mail(
        "отримано заявку на консультацію",
        settings.CUSTOM_DOMEN+link,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER,],
    )
    # TODO: сповіщення по SMS
    return JsonResponse({
        'status':'OK',
        # 'redirect':reverse('index'),
    })
