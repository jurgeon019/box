from django.conf import settings
from django.forms import TextInput, Textarea, NumberInput
from django.contrib import admin 
from django.shortcuts import reverse 
from django.utils.safestring import mark_safe
from django.urls import path 
from django.contrib import admin 
from django.conf import settings
from django.forms import TextInput, Textarea, NumberInput
from django.shortcuts import reverse 
from django.utils.safestring import mark_safe
from django.urls import path 
from django.conf import settings
from django.forms import TextInput, Textarea, NumberInput


from box.core.utils import (
    AdminImageWidget, show_admin_link, move_to, BaseAdmin,
    seo, base_main_info
)
from box.apps.sw_shop.sw_catalog.models import * 
from box.apps.sw_shop.sw_cart.models import * 
from box.apps.sw_shop.sw_catalog.models import * 
from box.apps.sw_shop.sw_cart.models import * 



from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin, TreeRelatedFieldListFilter
from modeltranslation.admin import *
from dal import autocomplete
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin


from .filters import * 
from .views import * 
from .item_inlines import * 
from ..resources import * 



class ItemManufacturerAdmin(
    TabbedTranslationAdmin,
    ImportExportActionModelAdmin,
    ImportExportModelAdmin,
    ):
    resource_class = ItemManufacturerResource
    search_fields = [
        'name'
    ]


class ItemUnitAdmin(TabbedTranslationAdmin):
    list_display = [
        'id',
        'name',
    ]
    list_display_links = list_display
    search_fields = [
        'name',
    ]


class ItemImageAdmin(
    # nested_admin.NestedTabularInline,
    BaseAdmin, 
    SortableAdminMixin,
    ):
    def get_model_perms(self, request):
        return {}

    def show_item(self, obj):
        return show_admin_link(obj=obj, obj_attr='item', obj_name='title')

    show_item.short_description = ('Товар')
    
    list_display = [
        'id',
        'show_image',
        'alt',
        'show_item',
    ]
    list_display_links = [
        'id',
        'alt',
    ]
    list_editable = []
    autocomplete_fields = [
        'item',
    ]


class ItemCurrencyAdmin(
    ImportExportModelAdmin,
    ImportExportActionModelAdmin,
    TabbedTranslationAdmin,
    ):
    resource_class = ItemCurrencyResource
    actions = [
        'delete',
    ]
    list_filter = []
    list_display = [
        # 'name',
        'code',
        'rate',
        'is_main',
    ]
    list_display_links = [
        # 'name',
        'code',
    ]
    list_editable = [
        'rate',
    ]
    readonly_fields = [
        # 'is_active',
        'is_main',
        # 'updated',
        # 'created',
        # 'code',
    ]
    formfield_overrides = {
        # models.CharField: {'widget': TextInput(attrs={'size':8})},
        # models.DecimalField: {'widget': NumberInput(attrs={"style":"width:70px"})}
    }
    search_fields = [
        # 'name',
        'code',
    ]



class ItemStockAdmin(TabbedTranslationAdmin):
    def get_model_perms(self, request):
        return {}

    list_display = [
        'id',
        'text',
        'availability',
        'colour',
    ] 
    list_display_links = [
        'id',
        'text',
    ] 
    fields = [
        # ''
    ]
    readonly_fields = [
        'created',
        'updated',
        # 'code',
    ]
    exclude = [
        'code',
        'order',
        "colour",
    ]
    list_editable = [
        'availability',
    ]
    search_fields = [
        'text',
    ]


class ItemMarkerAdmin(TabbedTranslationAdmin):
    def has_add_permission(self, request):
        return False 
    
    search_fields = [
        'text',
    ]
    fields = [
        'text',
    ]

class ItemLabelAdmin(TabbedTranslationAdmin):
    search_fields = [
        'text',
    ]
   


class ItemBrandAdmin(BaseAdmin, SortableAdminMixin, TabbedTranslationAdmin):
    # change_form
    fieldsets = [
        base_main_info,
        seo,
    ]
    prepopulated_fields = {
        'slug':('title',)
    }


class ItemReviewAdmin(
    BaseAdmin,
    # nested_admin.NestedTabularInline,
    ):
    list_display = [
        'id',
        'text',
        'phone',
        'email',
        'name',
        'is_active',
    ]
    list_display_links = [
        'id',
    ]
    list_filter = [
        'is_active',
    ]
    search_fields = [
        'text',
        'phone',
        'email',
        'name',
    ]


