from django.shortcuts import redirect 
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from ..models import *
from box.core.mail import box_send_mail 


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
      subject      = _('Отримано контактну форму'),
      template     = 'sw_contact_form/mail.html', 
      email_config = ContactRecipientEmail, 
      model        = model, 
      fail_silently= False,
    )
    return JsonResponse({
        'status':'OK',
    })






