from django.contrib import admin 
from ..models import * 


class ItemOptionInline(admin.StackedInline):
    model = ItemOption
    extra = 0 
    classes = [
        'collapse',
    ]