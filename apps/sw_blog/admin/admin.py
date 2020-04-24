from django.contrib import admin 
from django.urls import reverse 
from django.utils.html import mark_safe
from django.db import models 
from django.forms import NumberInput, Textarea, TextInput
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline

from ..models import *
from box.core.utils import (
    show_admin_link,
    AdminImageWidget, seo, 
)

class CommentInline(admin.StackedInline):
    model = PostComment
    extra = 0
    classes = ['collapse']


class PostInline(TranslationStackedInline):
    model = Post
    extra = 0
    classes = ['collapse']

from box.core.utils import BaseAdmin , seo 

class PostCategoryAdmin(BaseAdmin, TabbedTranslationAdmin):
    # changeform 
    fieldsets = (
        (('ОСНОВНА ІНФОРМАЦІЯ'), {
            'fields':(
                'title',
                'image',
                'created',
                'updated',
            ),
            'classes':('collapse'),
        }),
        seo,
    )
    prepopulated_fields = {
        "slug": ("title",),
    }
    save_on_top = True 
    # changelist
    search_fields = [
        'title',
        'description',
    ]
    list_display = [
        'id',
        'title',
        'slug',
        'is_active',
    ]
    list_display_links = [
        'id',
        'title',
        'slug',
    ]
    formfield_overrides = {
        models.CharField: {'widget': NumberInput(attrs={'size':'20'})},
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':6, 'cols':20})},
    }


from adminsortable.admin import SortableAdmin
from box.core.utils import BaseAdmin


class PostAdmin(
    BaseAdmin,
    TabbedTranslationAdmin,
    SortableAdmin,
    ):
    def show_category(self, obj):
      return show_admin_link(obj, obj_attr='category', obj_name='title')

    def show_image(self, obj):
        return mark_safe(f"<img src='{obj.image_url}' width='150px' height='auto'/>")

    show_category.short_description = _("Категорія")
    show_image.short_description    = _("Зображення")
  
    prepopulated_fields = {
        'slug':('title',),
    }
    autocomplete_fields = [
        'author',
        'category',
    ]
    inlines = [
        CommentInline,
    ]
    fieldsets = (
        (('ОСНОВНА ІНФОРМАЦІЯ'), {
            'fields':(
                'title',
                'content',
                'category',
                'author',
                # 'recomended',
                'image',
            ),
        }),
        seo,
    )

    list_display = [
        'show_image',
        'title',
        'show_category',
        'is_active',
        "show_site_link",
        'show_delete_link',
    ]
    list_editable = [
        'is_active',
    ]
    list_display_links = [
        'show_image',
        'title',
        "show_site_link",

    ]
    prepopulated_fields = {
        "slug": ("title",),
    }
    search_fields = [
        'title',
        'content',
    ]
    list_filter = [
        'category',
        'created',
        'updated',
    ]


class CommentAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]


class PostCommentAdmin(BaseAdmin):
    list_display = [
        'content',
        'is_active',
    ]
    list_display_links = [
        'content',
    ]
    search_fields = [
        'content',
    ]


