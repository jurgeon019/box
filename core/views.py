from django.views.defaults import (
  page_not_found, server_error, bad_request, permission_denied,
)
from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail 
from django.conf import settings 
from django.utils import translation
from box.core.sw_global_config.models import GlobalConfig
from . import settings as core_settings


def custom_bad_request(request, exception):
    return bad_request(request, exception, template_name=core_settings.PATH_400)


def custom_permission_denied(request, exception):
    return permission_denied(request, exception, template_name=core_settings.PATH_403)


def custom_page_not_found(request, exception):
    return page_not_found(request, exception, template_name=core_settings.PATH_404)


def custom_server_error(request):
    return server_error(request, template_name=core_settings.PATH_500)


def robots(request):
  robots = GlobalConfig.get_solo().robots_txt
  if robots:
    response = HttpResponse(robots)
  else:
    response = render(request, 'core/robots.txt', locals())
  return response


def set_lang(request, lang=None):
  translation.activate(lang)
  request.session[translation.LANGUAGE_SESSION_KEY] = lang
  # referer = request.META.get('HTTP_REFERER', '/uk/')
  referer = request.META['HTTP_REFERER']
  url = referer.split('/')
  url[3] = lang
  url = '/'.join(url)
  return redirect(url)


def testmail(request):
  if request.POST:
    send_mail(
      subject='123123123',
      message='123123123',
      from_email=settings.DEFAULT_FROM_EMAIL,
      recipient_list=['jurgeon018@gmail.com'],
      fail_silently=False,
    )

  return render(request, 'core/testmail.html', locals())


