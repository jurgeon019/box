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



class ItemCategoryAdmin(admin.ModelAdmin, ExportMixin):
    inlines = [
        # ItemInline,
        # ItemCategoryInline,
    ]
    actions = [
        'admin_export_categories_to_csv',
        
    ]
    list_display = [
        'id',
        'tree_title',
        # 'title',
        'slug',
        # 'code',
        'currency',
    ]
    search_fields = [
        'title',
        # 'id',
    ]
    list_display_links = [
        'id',
        'tree_title',
        # 'title',
        # 'slug',
    ]
    list_editable= [
        'currency',
    #     'slug'
    ]

    fieldsets = (
        ('ОСНОВНА ІНФОРМАЦІЯ', {
            "fields":(
                "title",
                'code',
                "thumbnail",
                "is_active",
                "created",
                'updated',
                'parent',
                "currency",
            ),
            'classes':(
                'wide',
            )
        }),
        ("SEO",{
            "fields":(
                (
                'meta_title',
                'meta_descr',
                'meta_key',
                ),
                "slug",
            ),
            'classes':(
                'collapse',
                'wide'
            )
        }),
    )
    readonly_fields = [
        'created',
        'updated',
    ]
    formfield_overrides = {
        models.CharField: {'widget': NumberInput(attrs={'size':'40'})},
        models.CharField: {'widget': TextInput(attrs={'size':'40'})},
        models.TextField: {'widget': Textarea(attrs={'rows':6, 'cols':20})},
    }
    prepopulated_fields = {
        "slug": ("title",),
    }

