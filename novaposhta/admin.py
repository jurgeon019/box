
from importlib import import_module

from django.apps import apps
from django.contrib import admin

from .models import Warehouse


def _get_warehouse_admin_base_class():
    if apps.is_installed('modeltranslation'):
        klass = import_module('modeltranslation.admin').TranslationAdmin
    klass = admin.ModelAdmin
    return klass


# TranslationAdmin = import_module('modeltranslation.admin').TranslationAdmin

from modeltranslation.admin import TabbedTranslationAdmin


# class WarehouseAdmin(_get_warehouse_admin_base_class()):
class WarehouseAdmin(TabbedTranslationAdmin):

    list_display = [
        'title',
        'address'
    ]
    search_fields = [
        'title',
        'address'
    ]


admin.site.register(Warehouse, WarehouseAdmin)



