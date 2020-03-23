from django.contrib import admin
from django.db import models 
from django.utils.html import mark_safe 
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline, TranslationStackedInline
from adminsortable.admin import SortableAdmin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

from .models import * 
# from .filters import * 
from .forms import * 
from .resources import * 

from box.core.utils import AdminImageWidget, move_to, BaseAdmin
from box.core.helpers import get_admin_url



from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter

from admin_auto_filters.filters import AutocompleteFilter 



class SliderFilter(AutocompleteFilter):
    title = 'слайдерами'
    field_name = 'slider'







class SlideInline(
    SortableInlineAdminMixin,
    TranslationStackedInline,
    ):
    model = Slide
    extra = 0 
    exclude = [
        'created',
        'updated',
        'page',
        'order',
        'text',
        'title',
        'alt',
        'code',
        'name',
        'is_active',
    ]
    readonly_fields = [
        # 'code',
    ]
    classes = [
        'collapse'
    ]
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }



class SliderAdmin(
    ImportExportActionModelAdmin,
    ImportExportModelAdmin, 
    admin.ModelAdmin,
    ):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, requets, obj=None):
        return False  
    save_on_top = True 
        
    resource_class = SliderResource
    list_display_links = [
        'name',
        'page',
    ]
    list_display = [
        'name',
        'page',
        # "show_delete_link",
    ]
    list_editable = [
    ]
    inlines = [
        SlideInline,
    ]
    fields = [
        # 'is_active', # шоб не попливла верстка лобацького, якшо вдруг дибіляка-клієнт вдруг захоче виключити слайдер 
        'name',
        'page',
        'created',
        'updated',
        'code',
    ]
    readonly_fields = [
        'created',
        'updated',
        'code',
    ]
    search_fields = [
        'name',
        'page',
        'code',
    ]
    autocomplete_fields = [
        'page',
        # 'category',
        # 'brand',
        # 'item',
    ]


class SlideAdmin(
    ImportExportActionModelAdmin,
    ImportExportModelAdmin, 
    SortableAdminMixin,
    TabbedTranslationAdmin,
    ):
    # change_list 
    resource_class = SlideResource
    # TODO: перенести цей шаблон в інші адмінки, де треба імпортувати і міняти порядок.
    change_list_template = 'core/sortable_import_export_change_list.html'
    save_on_top = True 

    def show_image(self, obj):
        return mark_safe(f"<img src='{obj.get_image_url()}' height='150' width='auto' />")

    def show_delete_link(self, obj):
        return mark_safe(f'<a href="/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.id}/change" style="color:red">x</a>')
    
    def show_slider_link(self, obj):
        return mark_safe(f'<a href="{get_admin_url(obj.slider)}">{obj.slider_name}</a>')

    show_delete_link.short_description = _("Видалити")
    show_slider_link.short_description = _("Посилання на слайдер")
    
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

    show_image.short_description = _("Зображення")
    change_slider.short_description = _('Перемістити в слайдер')
    actions = [
        "is_active_on",
        "is_active_off",
        'change_slider',  
    ]
    list_display = [
        'show_image',
        'name',
        "show_slider_link",
        'is_active',
        'show_delete_link',
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
        # 'text',
    ]
    formfield_overrides = {
        models.ImageField:{'widget':AdminImageWidget},
    }
