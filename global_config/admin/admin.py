from django.contrib import admin 
from django.db import models 
from django.forms import TextInput, Textarea


from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline, TranslationTabularInline

from ..models import * 
from ..forms import NotificationConfigForm

from box.solo.admin import SingletonModelAdmin
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
    change_form_template = 'des/change_form.html'
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
    # classes = ['collapse',]
    exclude = []


class SeoAdmin(SingletonModelAdmin):
    inlines = [
        SeoScriptInline,
    ]

