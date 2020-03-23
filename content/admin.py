from django.contrib import admin
from django.forms import Textarea
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin

from box.core.utils import AdminImageWidget

from .models import *
from .resources import *
from .filters import *
from .forms import PageAdminForm, TextAdminForm 




class TextInline(TranslationStackedInline):
    def has_add_permission(self,request, obj):
        return False 
    model = Img
    extra = 0
    classes = ['collapse']
    exclude = [
        'created',
        'updated',
    ]
    readonly_fields = [
        'code',
    ]

class ImgInline(TranslationStackedInline):
    def has_add_permission(self,request, obj):
        return False 
    model = Text
    classes = ['collapse']
    extra = 0
    exclude = [
        'created',
        'updated',
    ]
    readonly_fields = [
        'code',
    ]


class PageAdmin(
    ImportExportActionModelAdmin, 
    ImportExportModelAdmin,
    TabbedTranslationAdmin,
    ):
    resource_class = PageResource

    # def get_changelist_form(self, request, **kwargs):
    #     return PageAdminForm

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':'2', 'cols':'25'})},
    }
    

    inlines = [
        TextInline, 
        ImgInline,
    ]
    list_editable = [
        'meta_key',
    ]
    list_display = [
        'code',
        'meta_title',
        'meta_descr',
        'meta_key',
        'updated',
        'created',
    ]
    list_display_links = [
        'code',
        'meta_title',
        'meta_descr',
    ]
    search_fields = [
        'meta_title',
    ]
    exclude = [
        'image',
        'order',
        'alt',
        'description',
    ]
    readonly_fields = [
        'created',
        'updated',
    ]




class TextAdmin(
    ImportExportActionModelAdmin, 
    ImportExportModelAdmin,
    TabbedTranslationAdmin,
    ):
    list_per_page = 20 
    resource_class = TextResource
    list_display = [
        'code',
        'text',
        'updated',
        'created',
    ]
    readonly_fields = [
        'created',
        'updated',
        'code',

    ]
    list_display_links = [
        'code',
    ]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':19})},
    }
    # form = TextAdminForm
    list_filter = [ 
        'page',
        TextIsNoneFilter
    ]
    list_editable = [
        'text',
    ]
    search_fields = [
        'text',
    ]


class ImgAdmin(
    ImportExportActionModelAdmin, 
    ImportExportModelAdmin,
    TabbedTranslationAdmin,
    ):
    def show_image(self, obj):
        return mark_safe(f'<img src="{obj.image_url}" alt={obj.alt} style="max-width:150px; height:100px"/>')
    show_image.short_description = _("Картинка")
    resource_class = ImgResource
    list_display_links = [
        'code',
        'show_image',
        
    ]
    list_display = [
        'code',
        'show_image',
        'alt',
        'updated',
        'created',
    ]
    list_editable = [
        'alt',
    ]
    readonly_fields = [
        'updated',
        'created',
        'code',
    ]
    exclude  = [
        # 'page',
    ]
    formfield_overrides = {
        models.ImageField:{'widget':AdminImageWidget}
    }


admin.site.register(Img, ImgAdmin)
