from django.contrib import admin 
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin
import nested_admin
from ..models import *
from ..resources import CategoryResource, ItemResource


from .attribute import ItemAttributeInline 
from .feature import ItemFeatureInline 
from .option import ItemOptionInline 



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


class ItemAdmin(    
    ImportExportActionModelAdmin, 
    ImportExportModelAdmin,
    nested_admin.NestedModelAdmin,
    ):
    resource_class = ItemResource  
    inlines = [
        ItemAttributeInline,
        ItemFeatureInline,
        ItemOptionInline,
    ]



admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
