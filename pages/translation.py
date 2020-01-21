from modeltranslation.translator import (
    translator, TranslationOptions, register
)
from .models import *


# @register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = (
        'meta_title',
        'meta_descr',
        'meta_key',
    )


# @register(Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = (
        'value',
    )







