from django.shortcuts import render
from django.http import JsonResponse 



def handler_404(request, exception):
  return render(request,'404.html', locals())


def handler_500(request):
  return render(request,'500.html', locals())


def robots(request):
  return render(request, 'robots.txt', locals())


def help(request):
  response = {}
  response.update(shop_help) 
  response.update(blog_help) 
  return JsonResponse(response)

