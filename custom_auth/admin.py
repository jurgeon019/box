from django.contrib.auth.forms import (
    ReadOnlyPasswordHashWidget, ReadOnlyPasswordHashField,
    UsernameField, UserCreationForm,
    UserChangeForm, AuthenticationForm,
    PasswordResetForm, SetPasswordForm,
    AdminPasswordChangeForm,
)
from django.utils.translation import gettext, gettext_lazy as _
from django import forms 
from django.contrib import admin 
from django.contrib import admin 
from django.contrib.auth.models import (User, Group,)
from django.contrib.auth.admin import (UserAdmin, GroupAdmin,)

from box.shop.profile.models import (Profile,)
from box.shop.order.admin import (OrderInline,)

from box.custom_auth.models import User 



class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 1
    # def has_add_permission(self, request, obj=None):
    #     return True 


class CustomUserAdmin(UserAdmin):
    inlines = [
        # ProfileInline,
        # OrderInline,
    ]

    fieldsets = (
        (_('Personal info'), {
            'fields': (
                'first_name', 
                'last_name', 
                'email',
                'phone_number',
            )
        }),
        (None, {
            'fields': (
                'username', 
                'password'
            )
        }),
        # (_('Permissions'), {
        #     'fields': (
        #         'is_active', 
        #         'is_staff', 
        #         'is_superuser', 
        #         'groups', 
        #         'user_permissions'
        #     ),
        # }),
        # (_('Important dates'), {
        #     'fields': (
        #         'last_login', 
        #         'date_joined',
        #     ),
        # }),
    )
    readonly_fields = [
        # 'username',
        # 'first_name',
        # 'last_name',
        # 'email',
        # 'phone_number',
        # 'last_login',
        # 'date_joined',
    ]
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


    list_per_page = 100
    save_as_continue = False 
    save_on_top = True 

    list_display = (
        'id', 
        'username',
        'email',
        'first_name',
        'last_name',
        'phone_number',
    )
    list_display_links = [
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'phone_number',
    ]
    search_fields = [
        'email',
        'username',
        'first_name',
        'last_name',
        'phone_number',
    ]



class CustomGroup(GroupAdmin):
    exclude = []
