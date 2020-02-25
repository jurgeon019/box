from modeltranslation.admin import *

from django.conf import settings
from django.forms import TextInput, Textarea, NumberInput
from django.contrib import admin 
from django.shortcuts import reverse 
from django.utils.safestring import mark_safe
from django.urls import path 

from box.shop.item.models import * 
from box.shop.cart.models import * 
from box.shop.item.parser.main import *
from box.core.utils import AdminImageWidget


from ..inlines import * 


class ItemImageAdmin(admin.ModelAdmin):
    save_on_top = True 
    save_on_bottom = True 
    def headshot_image(self, obj):
        return mark_safe(
            f'<img \
                src="{obj.headshot.url}" \
                width="{obj.headshot.width}" \
                height={obj.headshot.height} \
            />'
        )
    def show_item(self, obj):
      option = "change" # "delete | history | change"
      massiv = []
      obj   = obj.item
      app   = obj._meta.app_label
      model = obj._meta.model_name
      url   = f'admin:{app}_{model}_{option}'
      href  = reverse(url, args=(obj.pk,))
      name  = f'{obj.title}'
      link  = mark_safe(f"<a href={href}>{name}</a>")
      return link
    def show_image(self, obj):
      option = "change" # "delete | history | change"
      massiv = []
      app   = obj._meta.app_label
      model = obj._meta.model_name
      url   = f'admin:{app}_{model}_{option}'
      href  = reverse(url, args=(obj.pk,))
      name  = f'{obj.image}'
      link  = mark_safe(f"<a href={href}>{name}</a>")
      return link
    show_item.short_description = ('Товар')
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

