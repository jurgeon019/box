from django.contrib import admin




class CustomAdmin(admin.AdminSite):
    site_header = "Site Admin"
    site_title  = "Site Admin"
    index_title = "Site Admin"

    

custom_admin = CustomAdmin(name='custom_admin')

from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
custom_admin.register(Redirect)
custom_admin.register(Site)


