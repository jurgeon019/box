from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from box.shop.help import help as shop_help 
from box.blog.help import help as blog_help 
from box.seo.models import Robots


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


def help(request):
  response = {}
  response.update(shop_help) 
  response.update(blog_help) 
  return JsonResponse(response)



