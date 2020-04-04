from django.conf import settings 
from django.contrib.sites.models import Site 
from django.core.mail import send_mail
from django.urls import reverse 

from box.core.sw_global_config.models import NotificationConfig


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
    recipient_list = settings.DEFAULT_RECIPIENT_LIST
  recipient_list.extend(NotificationConfig.get_solo().get_data('reverse')['emails'])
  print(recipient_list)
  send_mail(
    subject        = subject,
    message        = message,
    from_email     = from_email,
    recipient_list = recipient_list,
    fail_silently  = fail_silently,
  )
  # TODO: сповіщення по SMS




