from django.contrib import admin 
from django.utils.html import mark_safe 
from modeltranslation.admin import TabbedTranslationAdmin
from .filters import IsActiveFilter
from .models import *
from box.core.sw_solo.admin import SingletonModelAdmin
from .resources import * 


class ContactRecipientEmailInline(admin.TabularInline):
    extra = 0 
    model = ContactRecipientEmail
    exclude = []


@admin.register(ContactConfig)
class ContactConfigAdmin(SingletonModelAdmin):
    inlines = [
        ContactRecipientEmailInline,
    ]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    def show_link(self, obj):
        return mark_safe(f"<a href='{obj.url}'>{obj.url}</a>")

    def make_check_on(self, request, queryset):
        queryset.update(checked=True)

    def make_check_off(self, request, queryset):
        queryset.update(checked=False)

    make_check_on.short_description = ("Обробити")           
    make_check_off.short_description = ("Повернути до необроблених")           
    show_link.short_description = ("Ссилка")
    actions = [
        make_check_on,
        make_check_off,
    ]
    search_fields = [
        'name',
        'email',
        'phone',
        'message',
    ]
    list_filter = [
        # IsActiveFilter,
        'checked'
    ]
    list_display = [
        'name',
        'email',
        'phone',
        'message',
    ]
    exclude = [
        'url',
    ]
    readonly_fields = [
        'show_link'
    ]


