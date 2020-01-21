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


# @register(PageFeature)
class PageFeatureTranslationOptions(TranslationOptions):
    fields = (
        'value',
    )


@register(Member)
class MemberTranslationOptions(TranslationOptions):
    fields = [
        "meta_title",
        "meta_descr",
        "meta_key",
        "name",
        "description",
        "specialization",
    ]

@register(CaseCategory)    
class CaseCategoryTranslationOptions(TranslationOptions):
    fields = [
        "meta_title",
        "meta_descr",
        "meta_key",
        "title",
        "description",
    ]

@register(Case)    
class CaseTranslationOptions(TranslationOptions):
    fields = [
        "meta_title",
        "meta_descr",
        "meta_key",
        "title",
        "description",
    ]

@register(ServiceCategory)    
class ServiceCategoryTranslationOptions(TranslationOptions):
    fields = [
        "meta_title",
        "meta_descr",
        "meta_key",
        "title",
        "description",
    ]

@register(Service)    
class ServiceTranslationOptions(TranslationOptions):
    fields = [
        "meta_title",
        "meta_descr",
        "meta_key",
        "title",
        "description",
    ]








