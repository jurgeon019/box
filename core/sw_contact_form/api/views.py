from .serializers import * 
from django.shortcuts import redirect 
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings 
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.models import Site 

from ..models import *
from box.core.sw_global_config.models import GlobalConfig, GlobalRecipientEmail

from django.template.loader import render_to_string

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
    app_label       = model._meta.app_label
    model_name      = model._meta.model_name
    link            = reverse(f'admin:{app_label}_{model_name}_change', args=(model.id,))
    site            = 'https://'+Site.objects.get_current().domain + link 
    context         = {'contact':model, 'site':site}
    config          = GlobalConfig.get_solo()
    send_mail(
        subject='Отримано контактну форму',
        message=render_to_string('sw_contact_form/mail.html', context),
        from_email=config.from_email,
        recipient_list=GlobalRecipientEmail.get_recipient_list(),
    )
    return JsonResponse({
        'status':'OK',
        # 'url':'/'
        # 'redirect':reverse('index'),
    })







def box_send_mail(subject=None, message=None, from_email=None, recipient_list=None, fail_silently=False, model=None, *args, **kwargs):
  site = Site.objects.get_current().domain
  link = ''
  if model:
    app_label  = model._meta.app_label
    model_name = model._meta.model_name
    link       = reverse(f'admin:{app_label}_{model_name}_change', args=(model.id,))
  if not message:
    message = f'{site+link}'
  if not subject:
    subject = ' '
  if not from_email:
    from_email = settings.DEFAULT_FROM_EMAIL
  if not recipient_list:
    recipient_list = settings.DEFAULT_RECIPIENT_LIST or []
  # import pdb; pdb.set_trace();
  emails = GlobalConfig.get_solo().get_data('reverse')['emails']
  if emails:
     recipient_list.extend(emails)
  send_mail(
    subject        = subject,
    message        = message,
    from_email     = from_email,
    recipient_list = recipient_list,
    fail_silently  = fail_silently,
  )
  # TODO: сповіщення по SMS




