from modeltranslation.admin import *

from django.conf import settings
from django.forms import TextInput, Textarea, NumberInput
from django.contrib import admin 
from django.shortcuts import reverse 
from django.utils.safestring import mark_safe
from django.urls import path 

from box.shop.item.models import * 
from box.shop.cart.models import * 
from box.shop.item.parser.main import *
from box.core.utils import AdminImageWidget


from ..inlines import *
from ...views import * 

CURRENT_DOMEN = settings.CURRENT_DOMEN

def get_fieldsets():
    seo_fields = [
        'slug',
        (
        'meta_title',
        'meta_descr',
        'meta_key',
        ),
    ]
    seo_classes = [
        'collapse', 
        'wide',
        'extrapretty',
    ]
    item_classes = []
    item_fields = [
        (
        'in_stock',
        'is_active',
        ),
        (
        'title',
        'code',
        ),
        (
        'old_price',
        'new_price',
        'currency',
        ),
        'description',
        'thumbnail',
        # 'categories',
        'created',
        'updated',
    ]
    if settings.MULTIPLE_CATEGORY:
        item_fields.insert(-2 ,'categories')
    else:
        item_fields.insert(-2 ,'category')
    fieldsets = [
        [('ОСНОВНА ІНФОРМАЦІЯ'), {
            'fields':item_fields,
            'classes':item_classes,
        }],
        ['SEO', {
            'fields':seo_fields,
            'classes':seo_classes,
        }],
    ]
    return fieldsets


class ItemAdmin(TabbedTranslationAdmin, ExportMixin):
    actions = [
        # 'export_items',
        'admin_export_items_to_xlsx',
        "admin_export_items_photoes",
        "admin_delete_items_photoes",
        "admin_delete_items_features",
    ]
    change_list_template = 'item_change_list.html'
    change_form_template = 'item_change_form.html'
    # TODO: static method 
    fieldsets = get_fieldsets()
    formfield_overrides = {
        models.CharField: {'widget': NumberInput(attrs={'size':'20'})},
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':120})},
    }
    prepopulated_fields = {
        "slug": ("title",),
        "code": ("title",),
    }
    exclude = []
    readonly_fields = [
        'created',
        'updated',
    ]
    save_on_top = True 
    save_on_bottom = True 
    search_fields = [
        'title',
        'code',
        'slug',
        'description',
    ]
    list_filter = [
        "in_stock",
        "is_active", 
        "category",
    ]
    list_display = [
        'id',
        'title',
        # 'category',
        'price',
        'old_price',
        'in_stock',
        'is_active',
    ]
    list_editable = [
        # 'category',
    ]
    list_display_links = [
        'id', 
        'title',
    ]
    inlines = [
        ItemImageInline,
        ItemFeatureInline,
        ItemReviewInline, 
    ]
    list_per_page = 20


class CurrencyAdmin(admin.ModelAdmin):
    list_display_links = [
        'id',
        'name',
    ]
    list_display = [
        'id',
        'name',
        'is_main',
    ]


class CurrencyRatioAdmin(admin.ModelAdmin):
    list_display_links = [
        'id',
        'main',
        'compared',
        'ratio',
    ]
    list_display = [
        'id',
        'main',
        'compared',
        'ratio',
    ]


class ItemStockAdmin(admin.ModelAdmin):
    pass 

