from django.contrib import admin 
from box.admin import custom_admin 
from box.shop.profile.models import Profile 
from django.contrib.auth.models import User


# @admin.register(User, site=custom_admin)
# class UserAdmin(admin.ModelAdmin):
#     pass

@admin.register(Profile, site=custom_admin)
class ProfileAdmin(admin.ModelAdmin):
    pass

