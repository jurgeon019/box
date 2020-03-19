from django.conf import settings
from django.forms import TextInput, Textarea, NumberInput
from django.contrib import admin 
from django.shortcuts import reverse 
from django.utils.safestring import mark_safe
from django.urls import path 
from django.contrib import admin 
from django.conf import settings
from django.forms import TextInput, Textarea, NumberInput
from django.shortcuts import reverse 
from django.utils.safestring import mark_safe
from django.urls import path 
from django.conf import settings
from django.forms import TextInput, Textarea, NumberInput
from django.utils.translation import gettext_lazy as _


from box.core.utils import (
    AdminImageWidget, show_admin_link, move_to, BaseAdmin,
    seo, base_main_info
)
from box.shop.item.models import * 
from box.shop.cart.models import * 
from box.imp_exp.main import ExportMixin
from box.shop.item.models import * 
from box.shop.cart.models import * 


from .filters import * 
from .forms import * 
from .views import * 
from .resources import * 


from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin, TreeRelatedFieldListFilter
from modeltranslation.admin import *
from dal import autocomplete


class ItemImageInline(
    SortableInlineAdminMixin,
    TranslationTabularInline,
    ):
    model = ItemImage
    extra = 0
    classes = ['collapse']
    # def get_fields(self, request, obj):
    #     fields = [
    #         'image',
    #         # 'order',
    #         'alt',
    #     ]
    #     return fields 
    fields = [
        'image',
        'alt',
    ]
    readonly_fields = [
        'order',
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
        'old_price',
        'new_price',
        'currency',
    ]
    readonly_fields = [
        'show_title',
        'old_price',
        'new_price',
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
    fields = [
        'title',
        'is_active',
        'image',
        'slug',
    ]
    classes = ['collapse']
    verbose_name = _("підкатегорія")
    verbose_name_plural = _("підкатегорії")
    prepopulated_fields = {
        "slug": ("title",), 
    }
    formfield_overrides = {
        models.ImageField:{'widget':AdminImageWidget}
    }


class ItemOptionInline(
    TranslationTabularInline,
    ):
    model = ItemOption
    extra = 0 
    classes = [
        'collapse',
    ]


class BaseItemFeatureInline:
    model = ItemFeature
    # model = ItemFeature.items.through
    extra = 0 
    classes = ['collapse']
    
    exclude = [
        'code',
        'category',
        'categories',
    ]
    autocomplete_fields = [
        'name',
        'value',
    ]
    formfield_overrides = {
        # models.CharField: {'widget': NumberInput(attrs={'size':'20'})},
        models.CharField: {'widget': TextInput(attrs={'size':'50'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':70, 'style':'resize:vertical'})},
    }


class ItemFeatureTabularInline(BaseItemFeatureInline, TranslationTabularInline):
    pass 


class ItemFeatureStackedInline(BaseItemFeatureInline, TranslationStackedInline):
    pass 


class ItemCategoryAdmin(
    BaseAdmin, 
    SortableAdminMixin,
    DraggableMPTTAdmin, 
    TabbedTranslationAdmin, 
    ExportMixin,
    ):
    # changelist
    expand_tree_by_default = False 
    mptt_level_indent = 20 
    inlines = [
        ItemCategoryInline,
    ]
    actions = [
        "is_active_on",
        "is_active_off",
        'admin_export_categories_to_csv',
    ]
    list_display = [
        'tree_actions',
        "show_image",
        'indented_title',
        'is_active',
        'show_site_link',
        'show_delete_link',
    ]
    search_fields = [
        'title',
    ]
    list_display_links = [
        'indented_title',
    ]
    list_editable = [
        'is_active',
    ]
    list_filter = (
        # ('title', TreeRelatedFieldListFilter),
    )
    # changeform
    formfield_overrides = {
        models.ImageField:{'widget': AdminImageWidget},
        models.CharField: {'widget': NumberInput(attrs={'size':'40'})},
        models.CharField: {'widget': TextInput(attrs={'size':'40'})},
        models.TextField: {'widget': Textarea(attrs={'rows':6, 'cols':20})},
    }
    prepopulated_fields = {
        "slug": ("title",),
    }
    fieldsets = [
        [_('ОСНОВНА ІНФОРМАЦІЯ'), {
            "fields":[
                "title",
                'is_active',
                "currency",
                "image",
                'parent',
                'code',
                'description',
                "created",
                'updated',
            ]
        }],
        seo,
    ]
    readonly_fields = [
        'code',
        'created',
        'updated',
    ]
   

class ItemImageAdmin(BaseAdmin, SortableAdminMixin):
    def get_model_perms(self, request):
        return {}

    def show_item(self, obj):
        return show_admin_link(obj=obj, obj_attr='item', obj_name='title')

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
    list_editable = []
    autocomplete_fields = [
        'item',
    ]


def gen_item_fieldsets(self=None):
    item_fields = [
        (
        'amount',
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
        'image',
        # 'categories',
        'created',
        'updated',
    ]
    if settings.MULTIPLE_CATEGORY:
        item_fields.insert(-2 ,'categories')
    else:
        item_fields.insert(-2 ,'category')
    fieldsets = [
        [('ОСНОВНА ІНФОРМАЦІЯ'), {
            'fields':item_fields
        }],
        seo,
    ]
    return fieldsets


class ItemAdmin(
    BaseAdmin,
    TabbedTranslationAdmin, 
    ): 
    # changeform
    resource_class = ItemResource
    autocomplete_fields = [
        'brand',
        # 'similars',
        'in_stock',
    ]
    if settings.MULTIPLE_CATEGORY:
        autocomplete_fields.append('categories')
    else:
        autocomplete_fields.append('category')
    form = ItemForm
    fieldsets = gen_item_fieldsets()
    # change_list_template = 'item_change_list.html'
    # change_form_template = 'item_change_form.html'
    prepopulated_fields = {
        "slug": ("title",),
        "code": ("title",),
    }
    inlines = [
        ItemImageInline,
        ItemFeatureStackedInline,
        ItemOptionInline,
        ItemReviewInline, 
    ]  
    # changelist  
    def change_category(self, request, queryset):
        initial = {
            'model':ItemCategory,
            'attr':'category',
            'action_value':'change_category',
            'action_type':'add',
            'text':_('Нова категорія буде застосована для наступних позиций:'),
            'title':_("Зміна категорії"),
            'message':_('Категорія {0} була застосована до {1} товарів'),
        }
        return move_to(self, request, queryset, initial)

    def change_brand(self, request, queryset):
        initial = {
            'model':ItemBrand,
            'attr':'brand',
            'action_value':'change_brand',
            'action_type':'add',

            'text':_('Новий бренд буде застосований для наступних позиций:'),
            'title':_("Зміна бренду"),
            'message':_('Бренд {0} був застосований до {1} товарів'),
        }
        return move_to(self, request, queryset, initial)

    def add_markers(self, request, queryset):
        initial = {
            'model':ItemMarker,
            'attr':'markers',
            'action_value':'add_markers',
            'action_type':'add',
            'text':_('Нові маркери будуть застосовані для наступних позиций:'),
            'title':_("Додавання маркерів"),
            'message':_('Маркери {0} були застосовані до {1} товарів'),
        }
        return move_to(self, request, queryset, initial)
    
    def remove_markers(self, request, queryset):
        initial = {
            'model':ItemMarker,
            'attr':'markers',
            'action_value':'remove_markers',
            'action_type':'remove',
            'text':_('Нові маркери будуть забрані з наступних позиций:'),
            'title':_("Видалення маркерів з товарів"),
            'message':_('Маркери {0} були забрані з {1} товарів'),
        }
        return move_to(self, request, queryset, initial)

    change_category.short_description = ("Змінити категорію")
    add_markers.short_description     = ("Додати маркери")
    remove_markers.short_description  = ("Забрати маркери")
    change_brand.short_description    = ("Змінити бренд")
    actions = [
        "is_active_on",
        "is_active_off",
        # 'export_items',
        'admin_export_items_to_xlsx',
        "admin_export_items_photoes",
        "admin_delete_items_photoes",
        "admin_delete_items_features",
        "change_category",
        "change_brand",
        "add_markers",
        "remove_markers",
        'export_admin_action',
    ]
    search_fields = [
        'title',
        'code',
    ]
    list_filter = [
        # "category",
        # ('category', ItemCategoryTreeRelatedFieldListFilter),
        CategoryFilter,
        MarkersFilter,
        BrandFilter,
    ]
    list_display = [
        # 'id',
        "order",
        'show_image',
        'title',
        'new_price',
        'currency',
        'amount',
        'unit',
        # 'in_stock',
        'is_active',
        # "clone_link",
        'show_site_link',
        "show_edit_link",
        "show_delete_link",
    ]
    list_editable = [
        'new_price',
        'currency',
        'amount',
        # 'unit',
        # TODO: змінити ширину інпута
        'is_active',
    ]
    list_display_links = [
        'order',
        'title',
    ]


class ItemCurrencyAdmin(TabbedTranslationAdmin):
    list_display_links = [
        'id',
        'name',
    ]
    list_display = [
        'id',
        'name',
        'is_main',
    ]


class ItemCurrencyRatioAdmin(admin.ModelAdmin):
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


class ItemStockAdmin(TabbedTranslationAdmin):
    def get_model_perms(self, request):
        return {}

    list_display = [
        'id',
        'text',
        'availability',
        'colour',
    ] 
    list_display_links = [
        'id',
        'text',

    ] 
    list_editable = [
        'availability',
    ]
    search_fields = [
        'text',
    ]


class ItemFeatureAdmin(TabbedTranslationAdmin):
    search_fields = [
        'name',
    ] 


class ItemFeatureNameAdmin(TabbedTranslationAdmin):
    prepopulated_fields = {
        'slug':('name',),
    }
    search_fields = [
        'name',
    ] 


class ItemFeatureValueAdmin(TabbedTranslationAdmin):
    search_fields = [
        'value'
    ]


class ItemMarkerAdmin(TabbedTranslationAdmin):
    pass 
    # def get_model_perms(self, request):
    #     return {}


class ItemBrandAdmin(BaseAdmin, SortableAdminMixin, TabbedTranslationAdmin):
    # change_form
    fieldsets = [
        base_main_info,
        seo,
    ]
    prepopulated_fields = {
        'slug':('title',)
    }


class ItemReviewAdmin(BaseAdmin):
    list_display = [
        'id',
        'text',
        'phone',
        'email',
        'name',
        'is_active',
    ]
    list_display_links = [
        'id',
    ]
    list_filter = [
        'is_active',
    ]
    search_fields = [
        'text',
        'phone',
        'email',
        'name',
    ]


