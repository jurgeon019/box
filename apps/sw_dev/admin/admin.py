from ..resources import CategoryResource, ProductResource
from django.contrib import admin 
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin
import nested_admin



class ProductAttributeNameAdmin(admin.ModelAdmin):
    search_fields = [
        'name'
    ]



class ProductAttributeValueValueAdmin(admin.ModelAdmin):
    search_fields = [
        'value'
    ]


# class ProductAttributeValueInline(nested_admin.NestedTabularInline):
class ProductAttributeValueInline(nested_admin.NestedStackedInline):
    autocomplete_fields = [
        'value'
    ]
    extra = 0
    classes = [
        # 'collapse',
    ]
    # sortable_field_name = "attribute"
    model = ProductAttributeValue

# class ProductAttributeInline(nested_admin.NestedTabularInline):
class ProductAttributeInline(nested_admin.NestedStackedInline):
    autocomplete_fields = [
        'name'
    ]
    extra = 0
    classes = [
        # 'collapse',
    ]
    # sortable_field_name = "product"
    model = ProductAttribute
    inlines = [ProductAttributeValueInline]

class ProductAttributeAdmin(nested_admin.NestedModelAdmin):
    inlnes = [
        ProductAttributeValueInline
    ]

class ProductAttributeValueAdmin(nested_admin.NestedModelAdmin):
    pass 




import nested_admin

class CategoryAdmin(
    ImportExportActionModelAdmin, 
    ImportExportModelAdmin,
    DraggableMPTTAdmin,
    admin.ModelAdmin,
    ):
    resource_class = CategoryResource  
    list_display = [
        'tree_actions',
        'indented_title',
        'code',
    ]


class ProductAdmin(    
    ImportExportActionModelAdmin, 
    ImportExportModelAdmin,
    nested_admin.NestedModelAdmin,
    ):
    resource_class = ProductResource  
    inlines = [
        ProductAttributeInline,
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(ProductAttributeValue, ProductAttributeValueAdmin)
admin.site.register(ProductAttributeValueValue, ProductAttributeValueValueAdmin)
admin.site.register(ProductAttributeName, ProductAttributeNameAdmin)



