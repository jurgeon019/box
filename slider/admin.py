from django.contrib import admin
from django.db import models 
from django.utils.html import mark_safe 
from django.shortcuts import render, redirect


from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline, TranslationStackedInline
from adminsortable.admin import SortableAdmin

from .models import * 
from .filters import * 
from .forms import * 


from box.core.utils import AdminImageWidget, move_to, BaseAdmin



class SlideInline(TranslationStackedInline):
    model = Slide
    extra = 0 
    exclude = [
        'page',
    ]
    classes = [
        # 'collapse'
    ]
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }



class SliderAdmin(
    BaseAdmin,
    TabbedTranslationAdmin,
    SortableAdmin,
    ):
    list_display_links = [
        'name',
        'page',
    ]
    list_display = [
        'name',
        'page',
        'is_active',
        "show_delete_link",
    ]
    list_editable = [
        'is_active',
    ]
    inlines = [
        SlideInline,
    ]
    fields = [
        'name',
        "page",
        'is_active',
    ]
    autocomplete_fields = [
        'page',
        'category',
        'brand',
        'item',
    ]


class SlideAdmin(
    BaseAdmin,
    TabbedTranslationAdmin,
    SortableAdmin,
    ):
    # change_list 

    def show_image(self, obj):
        return mark_safe(f"<img src='{obj.get_image_url()}' height='150' width='auto' />")

    def change_slider(self, request, queryset):
        initial = {
            'model':Slider,
            'attr':'slider',
            'action_value':'change_slider',
            'action_type':'add',
            'text':_('Новий слайдер буде застосований для наступних позиций:'),
            'title':_("Додавання маркерів"),
            'message':_('Слайдер {0} був застосований до {1} слайдів'),
        }
        return move_to(self, request, queryset, initial)
    show_image.short_description = ("Зображення")
    change_slider.short_description =('Перемістити в слайдер')
    actions = [
        "is_active_on",
        "is_active_off",
        'change_slider',  
    ]
    list_display = [
        'show_image',
        'name',
        'slider',
        'is_active',
        'delete',
    ]
    list_display_links = [
        'show_image',
        'name',

    ]
    list_editable = [
        'is_active',
        # 'slider',
    ]
    list_filter = [
        # 'slider',
        SliderFilter
        # TODO: slider.is_active True or False
    ]
    # change_form
    save_on_top = True 
    search_fields = [
        'name',
    ]
    fields = [
        'name',
        'image',
        'slider',
        'is_active',
        'alt',
        'title',
        'text',
    ]
