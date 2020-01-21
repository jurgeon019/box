from django.contrib import admin
from django.forms import TextInput, Textarea


class CustomAdmin(admin.AdminSite):
    site_header = "Site Admin"
    site_title  = "Site Admin"
    index_title = "Site Admin"

    

custom_admin = CustomAdmin(name='custom_admin')

from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
custom_admin.register(Redirect)
custom_admin.register(Site)

class PageMixin:
    def get_fieldsets(self):
        fieldsets = [
            [['ПУБЛІКАЦІЯ'], {
                'fields':[
                    'title',
                    'image',
                    'created',
                    'updated',
                ],
                'classes':[
                    'collapse',
                    'wide', 
                    'extrapretty',
                ],
                # 'description':'123123123',
            }],
            [['SEO'], {
                'fields':[
                    'slug',
                    'alt',
                    [
                    'meta_title',
                    'meta_descr',
                    'meta_key',
                    ],
                ],
                'classes':[
                    'collapse', 
                    'wide', 
                    'extrapretty',
                ],
                # 'description':'321321321',
            }],
        ]
        return fieldsets
    
