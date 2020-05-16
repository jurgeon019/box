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
from django.views.i18n import set_language
from django.utils.translation import get_language


from django.urls import translate_url
from django.utils.translation import get_language_from_request, check_for_language
# def set_lang(request, lang=None):
def set_lang(request, new_lang, old_lang=None):
  # old_lang     = get_language_from_request(request, check_path=True)
  # old_lang     = get_language()
  default_lang = settings.LANGUAGE_CODE
  splitted     = request.META['HTTP_REFERER'].split('/')
  old_lang = default_lang
  if check_for_language(splitted[3]):
    old_lang = splitted[3]
  if   new_lang == old_lang and new_lang == default_lang:
    pass 
  elif (new_lang == old_lang and new_lang != default_lang) or (new_lang != old_lang and new_lang != default_lang):
    splitted[3] = new_lang
  elif new_lang != old_lang and new_lang == default_lang:
    del splitted[3]
  elif new_lang != old_lang and new_lang != default_lang:
    splitted.insert(3, new_lang)
  translation.activate(new_lang)
  request.session[translation.LANGUAGE_SESSION_KEY] = new_lang
  return redirect('/'.join(splitted))


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


