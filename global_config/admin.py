from django.contrib import admin 
from django.db import models 

from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline, TranslationTabularInline

from .models import * 
from .forms import NotificationConfigForm

from box.solo.admin import SingletonModelAdmin
from box.core.utils import AdminImageWidget



class SiteConfigAdmin(SingletonModelAdmin, TabbedTranslationAdmin):
    formfield_overrides = {
        models.ImageField:{'widget': AdminImageWidget}
    }


class NotificationConfigAdmin(SingletonModelAdmin):
    form = NotificationConfigForm
    change_form_template = 'des/change_form.html'
    class Media:
        js = ('js/des.js'),
        css = {
            'all': ('css/des.css',)
        }


class CalagoueConfigAdmin(SingletonModelAdmin):
    pass 




