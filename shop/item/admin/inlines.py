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





class ItemImageInline(TranslationTabularInline):
    
    model = ItemImage
    extra = 0
    classes = ['collapse']
    fields = [
        'image',
        'order',
        'alt',
    ]
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}


class ItemReviewInline(admin.TabularInline):
    model = ItemReview
    extra = 0 
    classes = ['collapse']
    exclude = [

    ]


class ItemInline(TranslationTabularInline):
    def show_title(self, obj):
      option = "change" # "delete | history | change"
      massiv = []
      app   = obj._meta.app_label
      model = obj._meta.model_name
      url   = f'admin:{app}_{model}_{option}'
      href  = reverse(url, args=(obj.pk,))
      name  = f'{obj.title}'
      link  = mark_safe(f"<a href={href}>{name}</a>")
      return link
    show_title.short_description = 'Товар'
    model = Item 
    extra = 0
    fields = [
        'show_title',
        'new_price',
        'old_price',
        'currency',
    ]
    readonly_fields = [
        'show_title',
        'new_price',
        'old_price',
        'currency',
    ]
    classes = ['collapse']
    # if settings.MULTIPLE_CATEGORY:
    #     filter_horizontal = [
    #         'categories',
    #     ]
    # else:
    #     filter_horizontal = [
    #         'category',
    #     ]


class ItemCategoryInline(TranslationStackedInline):
    model = ItemCategory 
    extra = 0
    exclude = [
        'meta_title',
        'meta_descr',
        'meta_key',
        'description',
        'code',
        'created',
        'updated',
    ]
    classes = ['collapse']
    verbose_name = "підкатегорія"
    verbose_name_plural = "підкатегорії"
    prepopulated_fields = {
        "slug": ("title",), 
    }


class ItemFeatureInline(TranslationTabularInline):
    model = ItemFeature
    extra = 0 
    classes = ['collapse']
    exclude = [
        'code',
        'category',
        'categories',
    ]
    formfield_overrides = {
        # models.CharField: {'widget': NumberInput(attrs={'size':'20'})},
        models.CharField: {'widget': TextInput(attrs={'size':'50'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':70, 'style':'resize:vertical'})},
    }
