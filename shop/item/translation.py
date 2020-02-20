from modeltranslation.translator import (
    translator, 
    TranslationOptions, 
    register
)
from .models import *



# @register(Item)
class ItemTranslationOptions(TranslationOptions):
    fields = (
        'meta_title',
        'meta_descr',
        'meta_key',
        'title',
        'description',
        'slug',
    )
translator.register(Item, ItemTranslationOptions)


# @register(ItemCategory)
class ItemCategoryTranslationOptions(TranslationOptions):
    fields = (
        'meta_title',
        'meta_descr',
        'meta_key',
        'title',
        'slug',
    )

translator.register(ItemCategory, ItemCategoryTranslationOptions)

# @register(Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = [
        'name',
        'value',
    ]


# @register(FeatureCategory)
class FeatureCategoryTranslationOptions(TranslationOptions):
    fields = [
        'name',
    ]


# @register(ItemImage)
class ItemImageTranslationOptions(TranslationOptions):
    fields = [
        'alt',
    ]




