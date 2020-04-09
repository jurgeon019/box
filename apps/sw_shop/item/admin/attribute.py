
from .imports import * 


class ItemFeatureNameAdmin(TabbedTranslationAdmin):
    prepopulated_fields = {
        'slug':('name',),
    }
    search_fields = [
        'name',
    ] 


class ItemFeatureValueAdmin(TabbedTranslationAdmin):
    search_fields = [
        'value'
    ]



class ItemFeatureAdmin(TabbedTranslationAdmin):
    search_fields = [
        'name',
    ] 

