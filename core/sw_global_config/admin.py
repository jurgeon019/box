from django.contrib import admin 
from django.db import models 
from django.forms import TextInput, Textarea


from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline, TranslationTabularInline

from .models import * 
from .forms import GlobalConfigForm

from box.core.sw_solo.admin import SingletonModelAdmin
from box.core.utils import AdminImageWidget



class SeoScriptInline(admin.TabularInline):
    model = SeoScript
    extra = 0
    exclude = []


class GlobalConfigAdmin(SingletonModelAdmin,TabbedTranslationAdmin):
    class Media:
        js = ('js/des.js'),
        css = {
            'all': ('css/des.css',)
        }
    form = GlobalConfigForm
    change_form_template = 'sw_global_config/des/change_form.html'
    formfield_overrides = {
        models.TextField:{'widget':Textarea(attrs={'cols':'30', 'rows':'1'})}
    }
    inlines = [
        SeoScriptInline,
    ]
    formfield_overrides = {
        models.ImageField:{'widget':AdminImageWidget}
    }


admin.site.register(GlobalConfig, GlobalConfigAdmin)

