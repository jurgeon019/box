from django.contrib import admin 
from django.db import models 
from django.forms import TextInput, Textarea


from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline, TranslationTabularInline

from .models import * 
from .forms import NotificationConfigForm

from box.core.sw_solo.admin import SingletonModelAdmin
from box.core.utils import AdminImageWidget



class SiteConfigAdmin(SingletonModelAdmin, TabbedTranslationAdmin):
    pass 


class NotificationConfigAdmin(SingletonModelAdmin):
    class Media:
        js = ('js/des.js'),
        css = {
            'all': ('css/des.css',)
        }
    form = NotificationConfigForm
    change_form_template = 'sw_global_config/des/change_form.html'
    formfield_overrides = {
        models.TextField:{'widget':Textarea(attrs={'cols':'30', 'rows':'1'})}
    }


class CatalogueConfigAdmin(SingletonModelAdmin):
    pass 


class DesignConfigAdmin(TabbedTranslationAdmin, SingletonModelAdmin):
    formfield_overrides = {
        models.ImageField:{'widget':AdminImageWidget}
    }


class RobotsAdmin(SingletonModelAdmin):
    pass 


class SeoScriptInline(admin.TabularInline):
    model = SeoScript
    extra = 0
    exclude = []


class SeoAdmin(SingletonModelAdmin):
    inlines = [
        SeoScriptInline,
    ]

admin.site.register(SiteConfig, SiteConfigAdmin)
admin.site.register(NotificationConfig, NotificationConfigAdmin)
admin.site.register(CatalogueConfig, CatalogueConfigAdmin)
admin.site.register(DesignConfig, DesignConfigAdmin)
# admin.site.register(Translation, TranslationAdmin)
admin.site.register(Robots, RobotsAdmin)
admin.site.register(Seo, SeoAdmin)

