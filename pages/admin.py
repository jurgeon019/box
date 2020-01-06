from django.contrib import admin
from django.forms import TextInput, Textarea

from project.admin import custom_admin
from pages.models import *


# INLINES 


class SliderInline(admin.TabularInline):
    model = Slider
    extra = 0


class IconInline(admin.TabularInline):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':70})},
    }
    model = Icon
    extra = 0


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
        'value',
    ]
    list_display = [
        "id",
        'code',
        'name',
        'value',
    ]
    readonly_fields = [
        'code',
        'name',
        
    ]
    exclude  = [
        'page',
    ]


@admin.register(Slider, site=custom_admin)
class SliderAdmin(admin.ModelAdmin):
    # def has_add_permission(self, request, obj=None):
    #     return False
    # def has_delete_permission(self, request, obj=None):
    #     return False
    list_display_links = [
        "id",
        'title',
        'text',
    ]
    list_display = [
        "id",
        'title',
        'text',
    ]
    exclude  = [
        'link',
        'page',
    ]


@admin.register(Icon, site=custom_admin)
class IconAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    list_display_links = [
        "id",
        'title',
        'text',
    ]
    list_display = [
        "id",
        'title',
        'text',
    ]
    exclude  = [
        'page',
    ]


@admin.register(Team, site=custom_admin)
class TeamAdmin(admin.ModelAdmin):
    list_display_links = [
        "id",
        'name',
        'position',
        'image',
        'alt',
    ]
    list_display = [
        "id",
        'name',
        'position',
        'image',
        'alt',
    ]
    exclude  = [
        'page',
    ]


