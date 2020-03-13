from django.contrib import admin
from django.db import models 
from django.utils.html import mark_safe 


from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline, TranslationStackedInline

from .models import * 

from box.core.utils import AdminImageWidget



class SlideInline(TranslationStackedInline):
    model = Slide
    extra = 0 
    exclude = [
        'page',
    ]

    def get_fields(self, obj):
        fields = super().get_fields(obj)
        fields += [
            # 'slider_url'
        ]
        return fields 
    classes = [
        # 'collapse'
    ]
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }



class SliderAdmin(TabbedTranslationAdmin):
    def is_active_on(self, request, queryset):
        queryset.update(is_active=True)
    def is_active_off(self, request, queryset):
        queryset.update(is_active=False)
    
    def delete(self, obj):
        return mark_safe(f"<a href='/admin/slider/slider/{obj.pk}/delete/' style='color:red'>x</a>")
    save_on_top = True 
    delete.short_description = ("Видалити")
    is_active_on.short_description = ("Увімкнути")
    is_active_off.short_description = ("Вимкнути")
    actions = [
        is_active_on,
        is_active_off,
    ]
    list_display = [
        'name',
        'page',
        'is_active',
        "delete",
    ]
    list_editable = [
        'is_active',
    ]
    inlines = [
        SlideInline,
    ]
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }
    fieldsets = [
        [None, {
            'fields':[
                'name',
                "page",
                'is_active',
            ],
        }],
    ]
    # filter_horizontal = [
    autocomplete_fields = [
        'page',
        'category',
        'brand',
        'item',
    ]


class SlideAdmin(TabbedTranslationAdmin):
    def show_image(self, obj):
        return mark_safe(f"<img src='{obj.get_image_url}' height='150' width='auto' />")
    def delete(self, obj):
        return mark_safe(f"<a href='/admin/slider/slide/{obj.pk}/delete/' style='color:red'>x</a>")
    show_image.short_description = ("Зображення")
    delete.short_description = ("Видалити")
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }
    search_fields = [
        'name',
    ]
    fieldsets = [
        [(""), {
            "fields":[
                'name',
                (
                'image',
                'slider',
                'is_active',
                ),
                # 'display',
                # 'mw_desc',
                # 'mh_desc',
                # 'mw_mob',
                # 'mh_mob',
                # "page",
                'alt',
                'title',
                'text',
            ],
        }],
    ]
    list_display = [
        'show_image',
        'name',
        'slider',
        'is_active',
        'delete',
    ]
    list_editable = [
        'is_active',
        'slider',
    ]
    list_filter = [
        'slider',
        # TODO: slider.is_active True or False
    ]
