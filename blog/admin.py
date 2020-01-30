from django.contrib import admin 
from box.admin import custom_admin
from box.blog.models import Post, PostCategory, PostComment
from django.urls import reverse 
from django.utils.html import mark_safe
from django.db import models 
from django.forms import NumberInput, Textarea, TextInput


class CommentInline(admin.StackedInline):
    model = PostComment
    extra = 0


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


@admin.register(PostCategory, site=custom_admin)
class PostCategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (('ОСНОВНА ІНФОРМАЦІЯ'), {
            'fields':(
                'title',
                'image',
                'created',
                'updated',
            ),
            'classes':(
                'collapse',
                'wide', 
                'extrapretty',

            ),
        }),
        (('SEO'), {
            'fields':(
                'slug',
                'alt',
                (
                'meta_title',
                'meta_descr',
                'meta_key',
                ),
            ),
            'classes':(
                'collapse', 
                'wide', 
                'extrapretty',
            ),
        }),
    )
    readonly_fields = [
        'created',
        'updated',
    ]
    list_display = [
        'id',
        'title',
        'slug',
    ]
    list_display_links = [
        'id',
        'title',
        'slug',
    ]
    exclude = [
        'created',
        'updated',
    ]
    formfield_overrides = {
        models.CharField: {'widget': NumberInput(attrs={'size':'20'})},
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':6, 'cols':20})},
    }
    prepopulated_fields = {
        "slug": ("title",),
    }
    save_on_top = True 



# @admin.register(Post, site=custom_admin)
class PostAdmin(admin.ModelAdmin):
    def show_category(self, obj):
      option = "change" # "delete | history | change"
      massiv = []
      obj   = obj.category
      link = ''
      if obj:
        app   = obj._meta.app_label
        model = obj._meta.model_name
        url   = f'admin:{app}_{model}_{option}'
        href  = reverse(url, args=(obj.pk,))
        name  = f'{obj.title}'
        link  = mark_safe(f"<a href={href}>{name}</a>")
      return link
    show_category.short_description = ("Категорія")
    inlines = [
        # CommentInline,
    ]
    fieldsets = (
        (('ОСНОВНА ІНФОРМАЦІЯ'), {
            'fields':(
                'title',
                'content',
                'category',
                # 'author',
                'image',
            ),
        }),
        (('SEO'), {
            'fields':(
                'slug',
                'alt',
                (
                'meta_title',
                'meta_descr',
                'meta_key',
                ),
            ),
            'classes':(
                'collapse', 
                'wide', 
                'extrapretty',
            ),
            # 'description':'321321321',

        }),
    )
    readonly_fields = [
        'created',
        'updated',
    ]
    list_display = [
        'id',
        'title',
        'show_category',
    ]
    list_display_links = [
        'id',
        'title',
    ]
    prepopulated_fields = {
        "slug": ("title",),
    }
    # formfield_overrides = {
    #     models.CharField: {'widget': NumberInput(attrs={'size':'20'})},
    #     models.CharField: {'widget': TextInput(attrs={'size':'20'})},
    #     models.TextField: {'widget': Textarea(attrs={'rows':6, 'cols':20})},
    # }
    save_on_top = True 
    search_fields = [
        'title',
        'content',
    ]
    list_filter = [
        'created',
        'updated',

    ]


# @admin.register(PostComment, site=custom_admin)
class CommentAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]

