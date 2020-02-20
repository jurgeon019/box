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
from modeltranslation.admin import TabbedTranslationAdmin

from django.conf import settings
from django.forms import TextInput, Textarea, NumberInput
from django.contrib import admin 
from django.shortcuts import reverse 
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget


from box.shop.item.models import * 
from box.shop.cart.models import * 
from .utils import ExportMixin
from box.admin import custom_admin


CURRENT_DOMEN = settings.CURRENT_DOMEN


class AdminImageWidget(AdminFileWidget):
  def render(self, name, value, attrs=None, renderer=None):
    output = []
    if value and getattr(value, "url", None):
      image_url = value.url
      file_name = str(value)
      output.append(
        f' <a href="{image_url}" target="_blank">'
        f'  <img src="{image_url}" alt="{file_name}" width="150" height="150" '
        f'style="object-fit: cover;"/> </a>')
    output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
    return mark_safe(u''.join(output))


class ItemImageInline(admin.TabularInline):
    
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
    if settings.MULTIPLE_CATEGORY:
        filter_horizontal = [
            'categories',
        ]
    else:
        filter_horizontal = [
            'category',
        ]


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


class ItemFeatureInline(admin.TabularInline):
    def save_model(self, request, obj, form, change):
        # obj.type=2
        # obj.save()
        print(obj)
        print(form)
        print(change)
    model = ItemFeature
    # model = ItemFeature.items.through
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


def get_fieldsets():
    seo_fields = [
        'slug',
        (
        'meta_title',
        'meta_descr',
        'meta_key',
        ),
    ]
    seo_classes = [
        'collapse', 
        'wide',
        'extrapretty',
    ]
    item_fields = []
    item_classes = []
    item_fields = [
        (
        'in_stock',
        'is_active',
        ),
        (
        'title',
        'code',
        ),
        (
        'old_price',
        'new_price',
        'currency',
        ),
        'description',
        'thumbnail',
        # 'categories',
        'created',
        'updated',
    ]
    if settings.MULTIPLE_CATEGORY:
        item_fields.insert(-2 ,'categories')
    else:
        item_fields.insert(-2 ,'category')
    fieldsets = [
        ['ОСНОВНА ІНФОРМАЦІЯ', {
            'fields':item_fields,
            'classes':item_classes,
        }],
        ['SEO', {
            'fields':seo_fields,
            'classes':seo_classes,
        }],
    ]
    return fieldsets



class ItemAdmin(TabbedTranslationAdmin, ExportMixin):
    pass 
    exclude = [
        'category',
    ]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    actions = [
        # 'export_items',
        'export_items_to_xlsx',
        "export_items_photoes",
        "delete_items_photoes",
        "delete_items_features",
    ]
    change_list_template = 'item_change_list.html'
    change_form_template = 'item_change_form.html'
    # TODO: static method 
    fieldsets = get_fieldsets()
    formfield_overrides = {
        models.CharField: {'widget': NumberInput(attrs={'size':'20'})},
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':120})},
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
        "is_active", 
        "category",
    ]
    list_display = [
        'id',
        'title',
        'category',
        'price',
        'old_price',
        'in_stock',
        'is_active',
    ]
    list_editable = [
        'category',
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


class ItemCategoryAdmin(admin.ModelAdmin):
    inlines = [
        # ItemInline,
        ItemCategoryInline,
    ]
    list_display = [
        'id',
        # 'tree_title',
        'title',
        'slug',
        'code',
        'currency',
    ]
    list_display_links = [
        'id',
        # 'tree_title',
        'title',
        'slug',
    ]
    list_editable= [
        'currency',
    #     'slug'
    ]

    fieldsets = (
        ('ОСНОВНА ІНФОРМАЦІЯ', {
            "fields":(
                "title",
                'code',
                "thumbnail",
                "is_active",
                "created",
                'updated',
                'parent',
                "currency",
            ),
            'classes':(
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


class ItemReviewAadmin(admin.ModelAdmin):
    pass


class CurrencyAdmin(admin.ModelAdmin):
    list_display_links = [
        'id',
        'name',
    ]
    list_display = [
        'id',
        'name',
        'is_main',
    ]


class CurrencyRatioAdmin(admin.ModelAdmin):
    list_display_links = [
        'id',
        'main',
        'compared',
        'ratio',
    ]
    list_display = [
        'id',
        'main',
        'compared',
        'ratio',
    ]

