from core.admin import custom_admin
from django.contrib import admin 
from django import forms 
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashWidget, ReadOnlyPasswordHashField,
    UsernameField, UserCreationForm,
    UserChangeForm, AuthenticationForm,
    PasswordResetForm, SetPasswordForm,
    AdminPasswordChangeForm,
)
from django.contrib import admin 
from shop.order.admin import (
    OrderInline,
)
from django.contrib.auth.models import (
    User,
    Group,
)
from django.contrib.auth.admin import (
    UserAdmin, 
    GroupAdmin,
)
from shop.profile.models import (
    Profile,
)
from .models import * 


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 1


# @admin.register(Profile, site=custom_admin)
class ProfileAdmin(admin.ModelAdmin):
    exclude = []


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        # fields = ('email', 'password',  'is_active')
        exclude = []
    def clean_password(self):
        return self.initial["password"]


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')


        
@admin.register(User, site=custom_admin)
class CustomUserAdmin(UserAdmin):
    # inlines = [
    #     ProfileInline,
    #     OrderInline,
    # ]
    def add_view(self, *args, **kwargs):
      self.inlines = []
      return super(UserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
      self.inlines = [ProfileInline]
      return super(UserAdmin, self).change_view(*args, **kwargs)
    list_per_page = 10
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


@admin.register(Group, site=custom_admin)
class CustomGroup(GroupAdmin):
    exclude = []
