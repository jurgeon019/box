from django.shortcuts import render
from django.http import HttpResponse 
from django.contrib.admin import AdminSite
from django.apps import apps 



def get_apps_list(request):
    models = apps.get_models()
    for model in models:
        # print(model)
        pass
    apps_list = AdminSite(name='admin').get_app_list(request)
    print(apps_list)
    return HttpResponse('ok')

