from django.contrib import admin 
from django import forms

from modeltranslation.admin import *

from box.solo.admin import SingletonModelAdmin
from box.core.utils import AdminImageWidget
from .models import * 



class DesignPhoneInline(admin.StackedInline):
    extra = 0 
    classes = ['collapse']
    model = DesignPhone


class DesignEmailInline(admin.StackedInline):
    extra = 0 
    classes = ['collapse']
    model = DesignEmail


class DesignSocialInline(admin.StackedInline):
    extra = 0 
    classes = ['collapse']
    model = DesignSocial


class DesignAddressInline(admin.StackedInline):
    extra = 0 
    classes = ['collapse']
    model = DesignAddress


class DesignConfigAdmin(TabbedTranslationAdmin, SingletonModelAdmin):
    formfield_overrides = {
        models.ImageField:{'widget':AdminImageWidget}
    }
    inlines = [
        DesignPhoneInline,
        DesignEmailInline,
        DesignSocialInline,
        DesignAddressInline,
    ]
   

