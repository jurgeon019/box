from modeltranslation.admin import *
from django.conf import settings
from django.forms import TextInput, Textarea, NumberInput
from django.contrib import admin 
from django.shortcuts import reverse 
from django.utils.safestring import mark_safe
from django.urls import path 

from box.shop.item.models import * 
from box.shop.cart.models import * 
from box.core.utils import AdminImageWidget


from .inlines import * 


from box.core.utils import show_admin_link




class ItemImageAdmin(admin.ModelAdmin):

    def show_image(self, obj):
        return show_admin_link(obj=obj, obj_image='image')

    def show_item(self, obj):
        return show_admin_link(obj=obj, obj_attr='item', obj_name='title')

    show_image.short_description = ('Зображення')
    show_item.short_description = ('Товар')
    
    save_on_top = True 
    save_on_bottom = True 
    list_display = [
        'id',
        'show_image',
        'alt',
        'show_item',
    ]
    list_display_links = [
        'id',
        'alt',
    ]

