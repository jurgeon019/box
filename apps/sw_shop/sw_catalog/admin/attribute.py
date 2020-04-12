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
from django.utils.translation import gettext_lazy as _


from box.core.utils import (
    AdminImageWidget, show_admin_link, move_to, BaseAdmin,
    seo, base_main_info
)
from box.apps.sw_shop.sw_catalog.models import * 
from box.apps.sw_shop.sw_cart.models import * 
from box.apps.sw_shop.sw_catalog.models import * 
from box.apps.sw_shop.sw_cart.models import * 


import nested_admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin, TreeRelatedFieldListFilter
from modeltranslation.admin import *
from dal import autocomplete
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin


from .filters import ItemFilter, CategoryFilter
from .views import * 
from .item_inlines import * 
from ..resources import * 



class ItemAttributeVariantInline(nested_admin.NestedTabularInline):
    autocomplete_fields = [
        'value'
    ]
    extra = 0
    classes = [
        'collapse',
    ]
    # sortable_field_name = "attribute"
    model = ItemAttributeVariant
    formfield_overrides = {
        models.TextField:{'widget':forms.Textarea(attrs={'cols':'35', 'rows':'1'})}
    }


class ItemAttributeInline(nested_admin.NestedTabularInline):
    autocomplete_fields = [
        'attribute'
    ]
    extra = 0
    classes = [
        'collapse',
    ]
    # sortable_field_name = "product"
    model = ItemAttribute
    inlines = [ItemAttributeVariantInline]


class ItemAttributeAdmin(nested_admin.NestedModelAdmin):
    class Media:
        pass
    inlines = [
        ItemAttributeVariantInline,
    ]
    autocomplete_fields = [
        'item',
        'attribute',
    ]
    list_filter = [
        'is_option',
        ItemFilter,
        AttributeFilter,
        # 'item',
    ]
    list_display = [
        'id',
        'is_option',
        'attribute',
        'item',
    ]
    list_display_links = [
        'id',
        'attribute',
        'item',
        'is_option',
    ]
    list_editable = [
        # 'is_option',
    ]
    search_fields = [
        'item',
    ]


class AttributeCategoryAdmin(TabbedTranslationAdmin):
    search_fields = [
        'name',
    ] 
    list_display = [
        'id',
        'name',
    ]
    list_display_links = [
        'id',
    ]
    list_editable = [
        'name',
    ]
    save_on_top = True 


class ItemAttributeVariantAdmin(nested_admin.NestedModelAdmin):
    class Media:
        pass
    def get_model_perms(self, request):
        return {}
    autocomplete_fields = [
        'item_attribute',
        'value',
    ] 
    list_display = [
        'id',
        'item_attribute',
        'price',
        'value',
    ]
    list_editable = [
        'value',
        'price',
    ]
    list_display_links = [
        'id',
        'item_attribute',
    ]
    list_filter = [
        ItemAttributeFilter,
    ]


class AttributeAdmin(
    TabbedTranslationAdmin,
    ImportExportActionModelAdmin,
    ImportExportModelAdmin,
    ):
    resource_class = AttributeResource
    # TODO: change category. проміжний action.
    search_fields = [
        'name'
    ]
    autocomplete_fields = [
        'category',
    ]
    list_display = [
        'id',
        
        'category',
        'name',
    ]
    list_display_links = [
        'id',
    ]
    list_editable = [
        'category',
        'name',
    ]
    list_filter = [
        CategoryFilter,

    ]


class AttributeVariantValueAdmin(TabbedTranslationAdmin):
    list_display = [
        'id',
        'value',
    ]
    list_editable = [
        'value',
    ]
    list_display_links = [
        'id',
    ]
    search_fields = [
        'value'
    ]



admin.site.register(ItemAttribute, ItemAttributeAdmin)
admin.site.register(ItemAttributeVariant, ItemAttributeVariantAdmin)
admin.site.register(AttributeVariantValue, AttributeVariantValueAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(AttributeCategory, AttributeCategoryAdmin)


