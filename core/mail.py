from django.conf import settings 
from django.contrib.sites.models import Site 
from django.core.mail import send_mail
from django.urls import reverse 
from django.template.loader import render_to_string

from box.core.sw_global_config.models import GlobalConfig, GlobalRecipientEmail


def box_send_mail(subject, template, email_config, model, fail_silently=False, context={}):
  site           = Site.objects.get_current().domain
  app_label      = model._meta.app_label
  model_name     = model._meta.model_name
  link           = reverse(f'admin:{app_label}_{model_name}_change', args=(model.id,))
  site           = 'https://'+Site.objects.get_current().domain + link 
  global_emails  = list(GlobalRecipientEmail.get_recipient_list())
  emails         = list(email_config.get_recipient_list())
  global_emails.extend(emails)
  context.update({'site':site, 'model':model})
  send_mail(
    subject        = subject,
    message        = render_to_string(template, context),
    from_email     = GlobalConfig.get_solo().from_email,
    recipient_list = set(global_emails),
    fail_silently  = fail_silently,
  )
  # TODO: сповіщення по SMS




