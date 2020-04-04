from django.contrib import admin 
from ..models import * 



class ItemSeoAdmin(admin.ModelAdmin):
    filter_horizontal = [
        'categories',
    ]
