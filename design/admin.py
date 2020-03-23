from django.contrib import admin 
from django import forms

from modeltranslation.admin import *

from box.solo.admin import SingletonModelAdmin
from box.core.utils import AdminImageWidget
from .models import * 



class DesignConfigAdmin(TabbedTranslationAdmin, SingletonModelAdmin):
    formfield_overrides = {
        models.ImageField:{'widget':AdminImageWidget}
    }
   

