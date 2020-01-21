from django.contrib import admin
from .models import *
from core.admin import custom_admin, PageMixin
 


@admin.register(Member, site=custom_admin)
class MemberAdmin(admin.ModelAdmin):
    list_editable = [
        'name'
    ]
    list_display_links = [
        'id',
    ]
    list_display = [
        'id',
        'name',
    ]

@admin.register(CaseCategory, site=custom_admin)
class CaseCategoryAdmin(admin.ModelAdmin):
    list_editable = [
        'title'
    ]
    list_display_links = [
        'id',

    ]
    list_display = [
        'id',
        'title',
    ]
    # fieldset

@admin.register(Case, site=custom_admin)
class CaseAdmin(admin.ModelAdmin):
    list_editable = [
        'title'
    ]
    list_display_links = [
        'id',

    ]
    list_display = [
        'id',
        'title',
    ]
    # fieldset

@admin.register(ServiceCategory, site=custom_admin)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_editable = [
        'title'
    ]
    list_display_links = [
        'id',

    ]
    list_display = [
        'id',
        'title',
    ]
    # fieldset

@admin.register(Service, site=custom_admin)
class ServiceAdmin(admin.ModelAdmin):
    list_editable = [
        'title'
    ]
    list_display_links = [
        'id',

    ]
    list_display = [
        'id',
        'title',
    ]
    # fieldset


@admin.register(MemberRequest, site=custom_admin)
class MemberAdmin(admin.ModelAdmin, PageMixin):
    list_display_links = [
        'id',
        'full_name'
    ]
    list_display = [
        'id',
        'full_name',
    ]
    def has_change_permission(self, request, obj=None):
        return False

