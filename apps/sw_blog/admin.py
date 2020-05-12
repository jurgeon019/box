from django.contrib import admin 
from django.urls import reverse 
from django.utils.html import mark_safe
from django.db import models 
from django.forms import NumberInput, Textarea, TextInput
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline
from box.core.utils import BaseAdmin , seo 
from adminsortable.admin import SortableAdmin
from box.core.utils import BaseAdmin
from .models import *
from box.core.utils import (
    show_admin_link,
    AdminImageWidget, seo, 
)
from django_summernote.admin import SummernoteModelAdmin
from markdownx.admin import MarkdownxModelAdmin



class CommentInline(admin.StackedInline):
    model = PostComment
    extra = 0
    classes = ['collapse']


class PostInline(TranslationStackedInline):
    model = Post
    extra = 0
    classes = ['collapse']


@admin.register(PostCategory)
class PostCategoryAdmin(
    BaseAdmin, 
    TabbedTranslationAdmin,
    # SummernoteModelAdmin,
    ):
    # summernote_fields = ('content',)
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



from import_export.admin import ImportExportModelAdmin
from .resources import PostResource



@admin.register(Post)
class PostAdmin(
    BaseAdmin,
    TabbedTranslationAdmin,
    SortableAdmin,
    ImportExportModelAdmin,
    # MarkdownxModelAdmin,
    # SummernoteModelAdmin,
    ):
    resource_class = PostResource
    def show_category(self, obj):
      return show_admin_link(obj, obj_attr='category', obj_name='title')

    def show_image(self, obj):
        return mark_safe(f"<img src='{obj.image_url}' width='150px' height='auto'/>")
    # summernote_fields = ('content',)
    show_category.short_description = _("Категорія")
    show_image.short_description    = _("Зображення")
  
    prepopulated_fields = {
        'slug':('title',),
    }
    autocomplete_fields = [
        'author',
        'category',
        'markers',
    ]
    inlines = [
        CommentInline,
    ]
    fieldsets = (
        seo,
        (('ОСНОВНА ІНФОРМАЦІЯ'), {
            'fields':(
                'title',
                'category',
                'author',
                'markers',
                'image',
                'content',
            ),
            # 'classes':['collapse']
        }),
        # (('КОНТЕНТ'), {
        #     'fields':(
        #         'content',
        #     ),
        #     # 'classes':['collapse',]
        # }),
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


# @admin.register(Comment)
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


