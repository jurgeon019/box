from django.contrib import admin 
from modeltranslation.admin import *
from .models import * 

from box.solo.admin import SingletonModelAdmin

from django import forms
from box.core.utils import AdminImageWidget



class DesignAdvantageInline(TranslationStackedInline):
    extra = 0 
    model = DesignAdvantage
    classes = ['collapse']


class DesignConfigAdmin(TabbedTranslationAdmin, SingletonModelAdmin):
    formfield_overrides = {
        models.ImageField:{'widget':AdminImageWidget}
    }
    inlines = [
        DesignAdvantageInline,
    ]
    fieldsets = [
        [(""), {
            "fields":[
                (
                    'logo',
                    'favicon',
                ),
                (
                    "delivery",
                    "payment",
                ),
            ],
            'classes':[
                # 'collapse',
                # 'wide',
                'extrapretty',
            ]
        }],
        [("Контакти"), {
            "fields":[
                "email",
                "phones",
                "time",
                "social",
            ],
            'classes':['collapse']
        }],
        [("Налаштування кольорів теми"), {
            "fields":[
                (
                "colour_buttons",
                "colour_buttons_text",
                "colour_buttons_hover",
                "colour_buttons_text_hover",
                ),
                (
                "colour_main",
                "colour_additional",
                "colour_main_background",
                "colour_additional_background",
                "colour_background",
                )
            ],
            "classes":['collapse']
        }]
    ]

from box.page.admin import PageFeatureAdmin
# class TranslationAdmin(TabbedTranslationAdmin):
class TranslationAdmin(admin.ModelAdmin):
# class TranslationAdmin(PageFeatureAdmin):
    pass 


