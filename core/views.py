from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail 
from django.conf import settings 
from django.utils import translation
from box.global_config.models import Robots


def handler_404(request, exception):
  return render(request,'404.html', locals())


def handler_500(request):
  return render(request,'500.html', locals())


def robots(request):
  robots = Robots.get_solo().robots_txt
  if robots:
    response = HttpResponse(robots)
  else:
    response = render(request, 'core/robots.txt', locals())
  return response


def set_lang(request, lang=None):
  translation.activate(lang)
  request.session[translation.LANGUAGE_SESSION_KEY] = lang
  # url = request.META.get('HTTP_REFERER', '/')#.split('/')
  # print(url)
  referer = request.META['HTTP_REFERER']
  print("referer: ", referer, '.')
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


