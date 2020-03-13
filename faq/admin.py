from django.contrib import admin 
from django.contrib.admin.actions import delete_selected

from modeltranslation.admin import TabbedTranslationAdmin
from adminsortable.admin import SortableAdmin

from .models import * 


class FaqAdmin(
    TabbedTranslationAdmin,
    SortableAdmin,
    ):
    def is_active_true(self, request, queryset):
        queryset.update(is_active=True)

    def is_active_false(self, request, queryset):
        queryset.update(is_active=False)

    is_active_true.short_description = ('Увімкнути')
    is_active_false.short_description = ('Вимкнути')
    delete_selected.short_description = ("Видалити")
    actions = [
        'is_active_false',
        'is_active_true',
    ]
    list_display = [
        'name',
        'is_active',
    ]
    list_display_links = [
        'name',
    ]
    list_editable = [
        'is_active',
    ]
