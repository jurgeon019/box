from django.contrib import admin 
import nested_admin
from ..models import *




class ItemAttributeValueInline(nested_admin.NestedStackedInline):
    autocomplete_fields = [
        'value'
    ]
    extra = 0
    classes = [
        # 'collapse',
    ]
    # sortable_field_name = "attribute"
    model = ItemAttributeValue

class ItemAttributeInline(nested_admin.NestedStackedInline):
    autocomplete_fields = [
        'name'
    ]
    extra = 0
    classes = [
        # 'collapse',
    ]
    # sortable_field_name = "product"
    model = ItemAttribute
    inlines = [ItemAttributeValueInline]

class ItemAttributeAdmin(nested_admin.NestedModelAdmin):
    inlnes = [
        ItemAttributeValueInline
    ]

class ItemAttributeValueAdmin(nested_admin.NestedModelAdmin):
    pass 


class ItemAttributeNameAdmin(admin.ModelAdmin):
    search_fields = [
        'name'
    ]



class ItemAttributeValueValueAdmin(admin.ModelAdmin):
    search_fields = [
        'value'
    ]
    

admin.site.register(ItemAttribute, ItemAttributeAdmin)
admin.site.register(ItemAttributeValue, ItemAttributeValueAdmin)
admin.site.register(ItemAttributeValueValue, ItemAttributeValueValueAdmin)
admin.site.register(ItemAttributeName, ItemAttributeNameAdmin)



