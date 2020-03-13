from django.contrib import admin 
from modeltranslation.admin import *
from .models import * 
from box.solo.admin import SingletonModelAdmin



class RobotsAdmin(SingletonModelAdmin):
    pass 


class SeoScriptInline(admin.TabularInline):
    model = SeoScript
    extra = 0
    # classes = ['collapse',]
    exclude = []


class SeoAdmin(SingletonModelAdmin):
    inlines = [
        SeoScriptInline,
    ]

class ItemSeoAdmin(admin.ModelAdmin):
    filter_horizontal = [
        'categories',
    ]
