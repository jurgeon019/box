from django.contrib import admin 
from django.db import models 
from django.forms import TextInput, Textarea
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin


from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline, TranslationTabularInline

from .models import * 
from .forms import GlobalConfigForm
from .resources import * 

from box.core.sw_solo.admin import SingletonModelAdmin
from box.core.utils import AdminImageWidget


class SeoScriptInline(admin.TabularInline):
    model = SeoScript
    extra = 0
    exclude = []



class GlobalTagInline(TranslationTabularInline):
    extra = 0 
    model = GlobalTag
    exclude = []
    

class GlobalRecipientEmailInline(admin.TabularInline):
    model = GlobalRecipientEmail
    extra = 0 
    exclude = []


class GlobalConfigAdmin(
    SingletonModelAdmin,
    TabbedTranslationAdmin,
    ImportExportModelAdmin,
    ):
    class Media:
        js = ('js/des.js'),
        css = {
            'all': ('css/des.css',)
        }
    # resource_class = GlobalConfigResource
    form = GlobalConfigForm
    change_form_template = 'sw_global_config/des/change_form.html'
    formfield_overrides = {
        models.TextField:{'widget':Textarea(attrs={'cols':'30', 'rows':'1'})}
    }
    inlines = [
        SeoScriptInline,
        GlobalTagInline, 
        GlobalRecipientEmailInline, 
    ]
    formfield_overrides = {
        models.ImageField:{'widget':AdminImageWidget}
    }


class GlobalTagAdmin(TabbedTranslationAdmin):
  def get_model_perms(self, request):
    return {}
  # model_perms = {}
  search_fields = [
    'name'
  ]



class GlobalMarkerAdmin(
    TabbedTranslationAdmin,
    ImportExportActionModelAdmin,
    ImportExportModelAdmin,
    ):

    def delete_queryset(self, request, queryset):
        queryset.filter(code__isnull=True).delete()
    
    def has_delete_permission(self, request, obj=None):
        return False if obj and obj.code else True 

    # def has_add_permission(self, request):
    #     return False 

    # def has_delete_permission(self, request, obj=None):
    #     return False 

    resource_class = GlobalMarkerResource
    
    search_fields = [
        'name',
    ]
    readonly_fields = [
        'code'
    ]
    fields = [
        'code',
        'name',
    ]

class GlobalLabelAdmin(
    TabbedTranslationAdmin,
    ImportExportActionModelAdmin,
    ImportExportModelAdmin,
    ):

    def has_add_permission(self, request):
        return False 

    def has_delete_permission(self, request, obj=None):
        return False 

    search_fields = [
        'text',
    ]
    readonly_fields = [
        'code'
    ]
    fields = [
        'text',
        'code',
    ]


class SeoScriptAdmin(ImportExportModelAdmin):
    resource_class = SeoScriptResource 

    
admin.site.register(GlobalConfig, GlobalConfigAdmin)
admin.site.register(GlobalTag, GlobalTagAdmin)
admin.site.register(GlobalMarker, GlobalMarkerAdmin)
admin.site.register(GlobalLabel, GlobalLabelAdmin)

