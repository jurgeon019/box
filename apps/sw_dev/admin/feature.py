from django.contrib import admin 
import nested_admin
from ..models import *



class ItemFeatureInline(admin.StackedInline):
    model = ItemFeature
    extra = 0
    classes = ['collapse']

class ItemFeatureAdmin(admin.ModelAdmin):
    pass 


class ItemFeatureValueAdmin(admin.ModelAdmin):
    pass 


class ItemFeatureNameAdmin(admin.ModelAdmin):
    pass 


admin.site.register(ItemFeature, ItemFeatureAdmin)
admin.site.register(ItemFeatureValue, ItemFeatureValueAdmin)
admin.site.register(ItemFeatureName, ItemFeatureNameAdmin)

