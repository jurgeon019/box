from import_export.admin import ImportExportModelAdmin

from django.contrib import admin 

from .models import *
from .resources import *

from box.core.sw_solo.admin import SingletonModelAdmin


@admin.register(LiqpayTransaction)
class LiqpayTransactionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False 
    
    def has_change_permission(self, request, obj=None):
        return False 
    


@admin.register(LiqpayConfig)
class LiqpayConfigAdmin(
    SingletonModelAdmin,
    ImportExportModelAdmin,
    ):
    resource_class = LiqpayConfigResource
    


