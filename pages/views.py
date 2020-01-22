from django.shortcuts import render 
from box.pages.models import Page 
from django.http import HttpResponse



def pages_generator(request, *args, **kwargs):
    param = kwargs['param']
    page,_  = Page.objects.get_or_create(code=param)
    return render(request, f'{param}.html', locals())


