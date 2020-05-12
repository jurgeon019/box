from django.contrib import admin 


from import_export.admin import (
    ImportExportActionModelAdmin, ImportExportModelAdmin
)
from modeltranslation.admin import TabbedTranslationAdmin

from .resources import *

from box.core.sw_solo.admin import SingletonModelAdmin


class ParseCurrencyInline(admin.TabularInline):
    model = ParseCurrency
    extra = 0 
    

@admin.register(ParseCurrency)
class ParseCurrencyAdmin(ImportExportModelAdmin):
    resource_class = ParseCurrencyResource
    exclude = ['config']
    def has_module_permission(self, request, obj=None):
        return {}


@admin.register(CurrencyConfig)
class CurrencyConfigAdmin(
    SingletonModelAdmin,
    ImportExportModelAdmin,
    ):
    # TODO: кнопка "спарсити валюти". 
    # Глянути як зроблено на sw_global_config з відправкою тестового мейла 
    resource_class = CurrencyConfigResource 
    inlines = [
        ParseCurrencyInline,
    ]


@admin.register(Currency)
class CurrencyAdmin(
    ImportExportModelAdmin,
    ImportExportActionModelAdmin,
    TabbedTranslationAdmin,
    ):
    
    resource_class = CurrencyResource
    list_filter = []
    list_display = [
        'code',
        'sale_rate',
        'purchase_rate',
        'is_main',
    ]
    list_display_links = [
        'code',
    ]
    list_editable = [
        'sale_rate',
        'purchase_rate',
    ]
    readonly_fields = [
        'is_main',
    ]
    search_fields = [
        'code',
    ]


