from django.contrib import admin
from .models import *
from core.admin import custom_admin


class PageFeatureInline(admin.TabularInline):
    model = PageFeature
    extra = 0
    exclude = [
        'code',
    ]
    readonly_fields = [
        'name',
    ]


# MODELS 


@admin.register(Page, site=custom_admin)
class PageAdmin(admin.ModelAdmin):
    inlines = [
        PageFeatureInline, 
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
    readonly_fields = [
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
    readonly_fields = [
        'code',
        'name',
        'page',
        
    ]
    exclude  = [
    ]


@admin.register(PageImage, site=custom_admin)
class PageImageAdmin(admin.ModelAdmin):
    list_display_links = [
        "id",
        'code',
        'name',
    ]
    list_display = [
        "id",
        'code',
        'name',
    ]
    readonly_fields = [
        'code',
        'name',
        
    ]
    exclude  = [
        'page',
    ]
