from django.contrib import admin 
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import (
    TranslationAdmin,
    TabbedTranslationAdmin,
    TabbedExternalJqueryTranslationAdmin,
    TabbedDjangoJqueryTranslationAdmin,
    TranslationTabularInline,
    TranslationStackedInline,
    TranslationGenericTabularInline,
    TranslationGenericStackedInline,
)
from django.conf import settings
from django.shortcuts import reverse 
from shop.item.models import * 
from shop.cart.models import * 
from project.admin import custom_admin
from django.forms import TextInput, Textarea, NumberInput



CURRENT_DOMEN = settings.CURRENT_DOMEN


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 0
    classes = ['collapse']
    exclude = [
        
    ]


class ItemReviewInline(admin.TabularInline):
    model = ItemReview
    extra = 0 
    classes = ['collapse']
    exclude = [

    ]


class ItemInline(admin.TabularInline):
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
    # filter_horizontal = ['category',]


class ItemCategoryInline(admin.TabularInline):
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


class ItemFeatureInline(admin.StackedInline):
    model = ItemFeature
    # model = ItemFeature.items.through
    extra = 0
    classes = ['collapse']
    exclude = [
        'code',
        'category',
    ]




@admin.register(Item, site=custom_admin)
# class ItemAdmin(TranslationAdmin, ImportExportModelAdmin):
# class ItemAdmin(TranslationAdmin):
# class ItemAdmin(TabbedExternalJqueryTranslationAdmin):
# class ItemAdmin(TabbedDjangoJqueryTranslationAdmin):
# class ItemAdmin(TabbedTranslationAdmin):
class ItemAdmin(admin.ModelAdmin):
    # class Media:
    #     js = (
    #         'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
    #         'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
    #         'modeltranslation/js/tabbed_translation_fields.js',
    #     )
    #     css = {
    #         'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
    #     }
    fieldsets = (
        ('ТОВАР', {
            'fields':(
                (
                'in_stock',
                'is_new',
                'is_active',
                ),
                (
                'title',
                'code',
                ),
                (
                'old_price',
                'new_price',
                # 'currency',
                ),
                'description',
                'category',
                'created',
                'updated',
            ),
            'classes':(
                'collapse',
                'wide', 
                'extrapretty',

            ),
            # 'description':'123123123',
        }),
        ('SEO', {
            'fields':(
                'slug',
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
    formfield_overrides = {
        models.CharField: {'widget': NumberInput(attrs={'size':'20'})},
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':6, 'cols':20})},
    }
    prepopulated_fields = {
        "slug": ("title",),
        "code": ("title",),
    }
    exclude = []
    readonly_fields = [
        'created',
        'updated',
    ]
    save_on_top = True 
    save_on_bottom = True 
    search_fields = [
        'title',
        'code',
        'slug',
        'description',
    ]
    list_filter = [
        "in_stock",
        "is_new", 
        "is_active", 
        "category",
    ]
    list_display = [
        'id',
        'title',
        'price',
        'old_price',
        'in_stock',
        # 'is_new',
        'is_active',
    ]
    list_display_links = [
        'id', 
        'title',
    ]
    inlines = [
        ItemImageInline,
        ItemFeatureInline,
        ItemReviewInline, 
    ]
    list_per_page = 20


@admin.register(ItemCategory, site=custom_admin)
class ItemCategoryAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline,
        ItemCategoryInline,
    ]
    fieldsets = (
        ('КАТЕГОРІЯ', {
            "fields":(
                "title",
                # "code",
                "is_active",
                "created",
                'updated',
                'parent',
            ),
            'classes':(
                'collapse',
                'wide',
            )
        }),
        ("SEO",{
            "fields":(
                (
                'meta_title',
                'meta_descr',
                'meta_key',
                ),
                "slug",
            ),
            'classes':(
                'collapse',
                'wide'
            )
        }),
    )
    readonly_fields = [
        'created',
        'updated',
    ]
    formfield_overrides = {
        models.CharField: {'widget': NumberInput(attrs={'size':'40'})},
        models.CharField: {'widget': TextInput(attrs={'size':'40'})},
        models.TextField: {'widget': Textarea(attrs={'rows':6, 'cols':20})},
    }
    prepopulated_fields = {
        "slug": ("title",),
    }


# @admin.register(ItemImage, site=custom_admin)
class ItemImageAdmin(admin.ModelAdmin):
    save_on_top = True 
    save_on_bottom = True 
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


@admin.register(ItemReview, site=custom_admin)
class ItemReviewAadmin(admin.ModelAdmin):
    pass
