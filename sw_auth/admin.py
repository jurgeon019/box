from django.contrib.auth.forms import (
    ReadOnlyPasswordHashWidget, ReadOnlyPasswordHashField,
    UsernameField, UserCreationForm,
    UserChangeForm, AuthenticationForm,
    PasswordResetForm, SetPasswordForm,
    AdminPasswordChangeForm,
)
from django.utils.translation import gettext, gettext_lazy as _
from django import forms 
from django.db import models 
from django.contrib import admin 
from django.contrib.auth.models import (User, Group,)
from django.contrib.auth.admin import (UserAdmin, GroupAdmin,)
from django.utils.html import mark_safe 
from django.shortcuts import reverse, render, redirect

from box.sw_shop.customer.models import (Customer,)
from box.sw_shop.order.admin import (OrderInline,)
from box.core.utils import move_to
from .resources import BoxUserResource

from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin



class BoxUserAdmin(
    ImportExportActionModelAdmin,
    ImportExportModelAdmin,
    UserAdmin,
    ):
    resource_class = BoxUserResource
    def change_group(self, request, queryset):
        initial = {
            'model':CustomerGroup,
            'attr':'group',
            'action_value':'change_group',
            'action_type':'add',
            'text':_('Нова група буде застосована для наступних позиций:'),
            'title':_("Додавання маркерів"),
            'message':_('Група {0} була застосована до {1} користувачів'),
        }
        return move_to(self, request, queryset, initial)
    def full_name(self, obj):
        full_name = obj.get_full_name()
        if not full_name:
            full_name = obj.username
        return full_name
    def show_delete_link(self, obj):
        app = obj._meta.app_label 
        model = obj._meta.model_name 
        url = f'admin:{app}_{model}_delete'
        href = reverse(url, args=(obj.pk,))
        link = mark_safe(f'<a href={href} style="color:red" >x</a>')
        return link 
    full_name.short_description = _("Назва")
    show_delete_link.short_description = _("Видалити")
    change_group.short_description = ("Перемістити у групу")
    def order_count(self, obj):
        count = obj.orders.all().count()
        return count
    actions = [
        change_group
    ]
    inlines = [
        OrderInline,
    ]
    fieldsets = (
        (_('Personal info'), {
            'fields': (
                'username', 
                'password',
                (
                'first_name', 
                'last_name', 
                ),
                (
                'email',
                'phone_number',
                ),
                (
                'address',
                'group',
                ),
            ),
            'classes':[
                'wide',
            ]
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser', 
                'groups', 
                'user_permissions'
            ),
            'classes':[
                'collapse'
            ]
        }),
        (_('Important dates'), {
            'fields': (
                'last_login', 
                'date_joined',
            ),
            'classes':[
                'collapse'
            ]
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': (
                'wide',
            ),
            'fields': (
                'username', 
                'password1', 
                'password2'
            ),
        }),
    )
    formfield_overrides = {
        models.TextField:{'widget':forms.Textarea(attrs={'rows':'2', 'cols':'33'})}
    }
    list_per_page = 100
    save_as_continue = False 
    save_on_top = True 

    autocomplete_fields = [
        # 'groups',
        # 'user_permissions',
        'group',
    ]
    readonly_fields = [
        'date_joined',
        'last_login',
    ]
    list_display = [
        'full_name',
        'email',
        'date_joined',
        'group',
        'order_count',
        "show_delete_link",
    ]
    list_display_links = list_display
    search_fields = [
        'email',
        'username',
        'first_name',
        'last_name',
        'phone_number',
    ]


class CustomGroup(GroupAdmin):
    exclude = []


