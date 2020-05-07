
from django.contrib import admin
from .models import *
from modeltranslation.admin import TabbedTranslationAdmin



class WarehouseAdmin(TabbedTranslationAdmin):

    list_display = [
        'title',
        'address'
    ]
    search_fields = [
        'title',
        'address'
    ]


class SettlementAdmin(TabbedTranslationAdmin):
    list_display = [
        'title',
        'region',
    ]
    search_fields = [
        "latitude",
        "longitude",
    ]


class AreaAdmin(TabbedTranslationAdmin):
    list_display = [
        'title',
    ]


class RegionAdmin(TabbedTranslationAdmin):
    list_display = [
        'id',
        'title',
        'area',
    ]



class TypeAdmin(TabbedTranslationAdmin):
    list_display = [
        'title',
    ]



admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Settlement, SettlementAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Region, RegionAdmin)




