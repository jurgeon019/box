from django.contrib import admin 
from django.contrib.admin.actions import delete_selected

from modeltranslation.admin import TabbedTranslationAdmin
from adminsortable2.admin import SortableAdminMixin

from .models import * 

from box.core.utils import BaseAdmin

class FaqAdmin(
    BaseAdmin,
    SortableAdminMixin,
    TabbedTranslationAdmin,
    ):
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

