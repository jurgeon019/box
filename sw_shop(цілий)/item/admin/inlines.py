
from .imports import * 
from django.utils.translation import gettext_lazy as _


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

