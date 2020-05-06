from django.contrib import admin 


from import_export.admin import (
    ImportExportActionModelAdmin, ImportExportModelAdmin
)
from modeltranslation.admin import TabbedTranslationAdmin

from .resources import *



class CurrencyAdmin(
    ImportExportModelAdmin,
    ImportExportActionModelAdmin,
    TabbedTranslationAdmin,
    ):
    resource_class = CurrencyResource
    actions = [
        'delete',
    ]
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

admin.site.register(Currency, CurrencyAdmin)
