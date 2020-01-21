from django.contrib import admin

from box.admin import custom_admin
from box.pages.models import *
from project.admin import SliderInline, IconInline


# INLINES 




class PageFeatureInline(admin.TabularInline):
    model = PageFeature
    extra = 0
    exclude = [
        'code',
    ]


# MODELS 


@admin.register(Page, site=custom_admin)
class PageAdmin(admin.ModelAdmin):
    inlines = [
        PageFeatureInline, 
        SliderInline,
        IconInline,
    ]
    list_display_links = [
        "id",
        'meta_title',
        'meta_descr',
        'meta_key',
        'code',
    ]
    list_display = [
        "id",
        'meta_title',
        'meta_descr',
        'meta_key',
        'code',
    ]

@admin.register(PageFeature, site=custom_admin)
class PageFeatureAdmin(admin.ModelAdmin):
    list_display_links = [
        "id",
        'code',
        'name',
        'page',
    ]
    list_display = [
        "id",
        'code',
        'name',
        'page',
        'value',
    ]
    list_editable = [
        'value'
    ]
    exclude  = [
    ]


@admin.register(PageImage, site=custom_admin)
class PageImageAdmin(admin.ModelAdmin):
    list_display_links = [
        "id",
        'code',
        'name',
        'value',
    ]
    list_display = [
        "id",
        'code',
        'name',
        'value',
    ]
    exclude  = [
        'page',
    ]

