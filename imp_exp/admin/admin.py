from django.contrib import admin 
from django.shortcuts import render, redirect, reverse 
from django.urls import path 
from django.http import HttpResponse, JsonResponse

from modeltranslation.admin import *

from .models import * 


class ImportLogAdmin(admin.ModelAdmin):
    pass


class ImportAdmin(admin.ModelAdmin):

    def get_example(self, request):
        # context = dict(
        #    self.admin_site.each_context(request),
        #    key=value,
        # )
        # print(context)
        response = HttpResponse(content_type='text/csv')
        response
        response['Content-Disposition'] = 'attachment; filename="example.csv"'
        return response

    def get_urls(self):
        urls = [
            # path('get_example/', self.get_example, name='get_example'),
            path('get_example/', self.admin_site.admin_view(self.get_example), name='get_example'),
        ]
        urls = urls + super().get_urls()
        return urls

    change_list_template = 'imp_exp/admin/import_change_list.html'



class ExportAdmin(admin.ModelAdmin):
    change_list_template = 'imp_exp/admin/export_change_list.html'


# admin.site.register(Import, ImportAdmin)
# admin.site.register(Export, ExportAdmin)

