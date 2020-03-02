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
    )
translator.register(Item, ItemTranslationOptions)


# @register(ItemCategory)
class ItemCategoryTranslationOptions(TranslationOptions):
    fields = (
        'meta_title',
        'meta_descr',
        'meta_key',
        'title',
    )

translator.register(ItemCategory, ItemCategoryTranslationOptions)

# @register(ItemFeature)
class ItemFeatureTranslationOptions(TranslationOptions):
    fields = [
        'name',
        'value',
    ]

translator.register(ItemFeature, ItemFeatureTranslationOptions)

@register(ItemFeatureCategory)
class ItemFeatureCategoryTranslationOptions(TranslationOptions):
    fields = [
        'name',
    ]


@register(ItemImage)
class ItemImageTranslationOptions(TranslationOptions):
    fields = [
        'alt',
    ]


translator.register(ItemStock, fields=[
    'text',
])


