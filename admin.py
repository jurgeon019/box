from django.contrib import admin
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.contrib.auth.models import (User, Group,)
from django.contrib.auth.admin import (UserAdmin, GroupAdmin,)


class CustomAdmin(admin.AdminSite):
    site_header = "Site Admin"
    site_title  = "Site Admin"
    index_title = "Site Admin"


custom_admin = CustomAdmin(name='custom_admin')


class AdminPlus(admin.AdminSite):
    site_header = "Site Admin"
    site_title  = "Site Admin"
    index_title = "Site Admin"


admin_plus = AdminPlus(name='admin_plus')
admin_plus.register(Redirect)
admin_plus.register(Site)
admin_plus.register(User, UserAdmin)
admin_plus.register(Group, GroupAdmin)

