from django.contrib import admin 
from django import forms 
import nested_admin
from ..models import *
from modeltranslation.admin import TabbedTranslationAdmin



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
        models.TextField:{'widget':forms.Textarea(attrs={'cols':'10', 'rows':'1'})}
    }


class ItemAttributeInline(nested_admin.NestedTabularInline):
    autocomplete_fields = [
        'attribute'
    ]
    extra = 0
    classes = [
        'collapse',
    ]
    formfield_overrides = {
        models.TextField:{'widget':forms.Textarea(attrs={'cols':'10', 'rows':'1'})}
    }
    # sortable_field_name = "product"
    model = ItemAttribute
    inlines = [ItemAttributeVariantInline]


class ItemAttributeAdmin(nested_admin.NestedModelAdmin):
    inlnes = [
        ItemAttributeVariantInline
    ]

class AttributeCategoryAdmin(TabbedTranslationAdmin):
    pass 



class ItemAttributeVariantAdmin(nested_admin.NestedModelAdmin):
    pass 


class AttributeAdmin(TabbedTranslationAdmin):
    search_fields = [
        'name'
    ]


class ItemAttributeVariantValueAdmin(admin.ModelAdmin):
    search_fields = [
        'value'
    ]
    

AttributeCategory
admin.site.register(ItemAttribute, ItemAttributeAdmin)
admin.site.register(ItemAttributeVariant, ItemAttributeVariantAdmin)
admin.site.register(ItemAttributeVariantValue, ItemAttributeVariantValueAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(AttributeCategory, AttributeCategoryAdmin)


