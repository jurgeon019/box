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
from box.core.utils import AdminImageWidget, show_admin_link

from .filters import * 
from .inlines import *
from .forms import * 
from ..views import * 

from box.custom_admin.modelclone import ClonableModelAdmin
CURRENT_DOMEN = settings.CURRENT_DOMEN


from adminsortable.admin import SortableAdmin



class ImageWidgetAdmin(admin.ModelAdmin):
    image_fields = []

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.image_fields:
            request = kwargs.pop("request", None)
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(ImageWidgetAdmin, self).formfield_for_dbfield(db_field, **kwargs)


def gen_fieldsets(self=None):
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
    item_classes = []
    item_fields = [
        'similars',
        'brand',
        (
        'amount',
        'in_stock',
        'is_active',
        ),
        (
        'title',
        'code',
        # 'features',
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
        [('ОСНОВНА ІНФОРМАЦІЯ'), {
            'fields':item_fields,
            'classes':item_classes,
        }],
        ['SEO', {
            'fields':seo_fields,
            'classes':seo_classes,
        }],
    ]
    return fieldsets


class ItemAdmin(
    SortableAdmin, 
    ClonableModelAdmin, 
    TabbedTranslationAdmin, 
    ExportMixin,
    AdminImageWidget,
    ):

    def add_view(self,request,extra_content=None):
        self.inlines = [
            ItemImageInline,
            #    ItemFeatureInline,
            ItemFeatureStackedInline,
            ItemReviewInline, 
        ]
        return super().add_view(request)

    def change_view(self,request,object_id,extra_content=None):
        self.inlines = [
            ItemImageInline,
            ItemFeatureTabularInline,
            #    ItemFeatureInline,
            ItemReviewInline, 
        ]
        return super().change_view(request,object_id)
    
    def get_thumbnail_url(self, obj):
        return mark_safe(f"<img src='{obj.thumbnail_url}' height='auto' width='100' />")
    
    def view_button(self, obj):
        if obj.is_active:
            return mark_safe(f"<a href='{obj.get_absolute_url()}'>Переглянути</a>")
        return "Товар не активний"

    def change_button(self, obj):
        return mark_safe(f'<a href="/admin/item/item/{obj.id}/change/">Змінити</a>')

    def delete_button(self, obj):
        return mark_safe(f'<a href="/admin/item/item/{obj.id}/delete/">Видалити</a>')

    def move_to_category(self, request, queryset):
        form = None 
        if 'apply' in request.POST:
            form = ChangeCategoryForm(request.POST)
            if form.is_valid():
                category = form.cleaned_data['category']
                count = 0 
                for item in queryset:
                    item.category = category 
                    item.save()
                    count += 1
            self.message_user(request, f'Категорія {category} була застосована до {count} товарів')
            return redirect(request.get_full_path())
        if not form:
            form = ChangeCategoryForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
            return render(request, 'item/admin/move_to_category.html', {
                'items':queryset, 'form':form, 'title':'Зміна категорії'
            })

    def move_to_brand(self, request, queryset):
        form = None 
        if 'apply' in request.POST:
            form = ChangeBrandForm(request.POST)
            if form.is_valid():
                brand = form.cleaned_data['brand']
                count = 0 
                for item in queryset:
                    item.brand = brand 
                    item.save()
                    count += 1 
            self.message_user(request, f'Бренд {brand} була застосована до {count} товарів')
            return redirect(request.get_full_path())
        if not form:
            form = ChangeBrandForm(initial={'_selected_action':request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
            return render(request, 'item/admin/move_to_brand.html', {
                "items":queryset, "form":form, "title":"Зміна бренду"
            })

    def move_to_markers(self, request, queryset):
        form = None 
        if 'apply' in request.POST:
            form = ChangeMarkersForm(request.POST)
            if form.is_valid():
                markers = form.cleaned_data['markers']
                count = 0 
                for item in queryset:
                    for marker in markers:
                        item.markers.add(marker) 
                        item.save()
                        count += 1 
            self.message_user(request, f'Маркери {markers} була застосована до {count} товарів')
            return redirect(request.get_full_path())
        if not form:
            form = ChangeMarkersForm(initial={'_selected_action':request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
            return render(request, 'item/admin/move_to_markers.html', {
                "items":queryset, "form":form, "title":"Зміна бренду"
            })

    change_button.short_description = ("Змінити")    
    delete_button.short_description = ("Видалити")    
    view_button.short_description   = ("Переглянути ")
    move_to_category.short_description = ("Змінити категорію")
    move_to_markers.short_description = ("Змінити Маркер")
    move_to_brand.short_description = ("Змінити бренд")


    autocomplete_fields = [
        'brand',
        # 'category',
        'categories',
        'similars',
    ]
    get_thumbnail_url.allow_tags = True 
    get_thumbnail_url.short_description = ("Зображення")
    fieldsets = gen_fieldsets()
    
    actions = [
        # 'export_items',
        'admin_export_items_to_xlsx',
        "admin_export_items_photoes",
        "admin_delete_items_photoes",
        "admin_delete_items_features",
        "admin_is_active_on",
        "admin_is_active_off",
        "move_to_category",
        "move_to_brand",
        "move_to_markers",
    ]
    change_list_template = 'item_change_list.html'
    change_form_template = 'item_change_form.html'
    # TODO: static method 
    # formfield_overrides = {
    #     models.CharField: {'widget': NumberInput(attrs={'size':'20'})},
    #     models.CharField: {'widget': TextInput(attrs={'size':'20'})},
    #     models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':120})},
    # }
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
        # "category",
        # ('category', ItemCategoryTreeRelatedFieldListFilter),
        CategoryFilter,
        MarkersFilter,
        BrandFilter,

    ]
    form = ItemForm
    list_display = [
        # 'id',
        "order",
        'get_thumbnail_url',
        'title',
        'new_price',
        'currency',
        'amount',
        'unit',
        # 'in_stock',
        'is_active',
        "clone_link",
        'view_button',
        "change_button",
        "delete_button",
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
        # 'id', 
        'order',
        'title',
    ]
    list_per_page = 20
    exclude = [
        'items',
    ]
    filter_horizontal = [
    # filter_vertical = [
        # 'similars',
    ]

from dal import autocomplete

class many_to_many_field_Autocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # qs = *custom query if needed*
        #search option
        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


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


class ItemFeatureNameAdmin(TabbedTranslationAdmin):
    prepopulated_fields = {
        'slug':('name',),
    }
    search_fields = [
        'name',
    ] 


class ItemMarkerAdmin(TabbedTranslationAdmin):
    pass 


class ItemBrandAdmin(TabbedTranslationAdmin):
    search_fields = [
        'name',
    ]


