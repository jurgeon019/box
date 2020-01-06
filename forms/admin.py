from django.contrib import admin 
from forms.models import ContactRequest, CreditRequest, OrderRequest
from project.admin import custom_admin
from django.urls import reverse 
from django.utils.html import mark_safe 



@admin.register(ContactRequest, site=custom_admin)
class ContactRequestAdmin(admin.ModelAdmin):
    def has_add_permission(self, obj, request=None):
        return False 
    list_display = [
        'id',
        'name',
        'phone',
        'email',
        'message',
        'created',
    ]
    list_display_links = [
        'id',
        'name',
        'phone',
        'email',
        'message',
        'created',
    ]
    fields  = [
        'name',
        'phone',
        'email',
        'message',
    ]
    readonly_fields = fields



@admin.register(CreditRequest, site=custom_admin)
class CreditRequestAdmin(admin.ModelAdmin):
    def has_add_permission(self, obj, request=None):
        return False 
    def show_item(self, obj):
      option = "change" # "delete | history | change"
      obj   = obj.item 
      app   = obj._meta.app_label
      model = obj._meta.model_name
      url   = f'admin:{app}_{model}_{option}'
      href  = reverse(url, args=(obj.pk,))
      name  = f'{obj.title}'
      link  = mark_safe(f"<a href={href}>{name}</a>")
      return link
    show_item.short_description = 'Товар'

    list_display = [
        'id',
        'item',
        'name',
        'phone',
        'email',
        'created',
    ]
    list_display_links = [
        'id',
        'item',
        'name',
        'phone',
        'email',
        'created',
    ]
    fields  = [
        'show_item',
        'name',
        'phone',
        'email',
    ]
    readonly_fields = fields 




@admin.register(OrderRequest, site=custom_admin)
class OrderRequestAdmin(admin.ModelAdmin):
    def has_add_permission(self, obj, request=None):
        return False 
    def show_item(self, obj):
      option = "change" # "delete | history | change"
      obj   = obj.item 
      app   = obj._meta.app_label
      model = obj._meta.model_name
      url   = f'admin:{app}_{model}_{option}'
      href  = reverse(url, args=(obj.pk,))
      name  = f'{obj.title}'
      link  = mark_safe(f"<a href={href}>{name}</a>")
      return link
    show_item.short_description = 'Товар'

    list_display = [
        'id',
        'item',
        'name',
        'phone',
        'email',
        'created',
    ]
    list_display_links = [
        'id',
        'item',
        'name',
        'phone',
        'email',
        'created',
    ]
    fields  = [
        'show_item',
        'name',
        'phone',
        'email',
    ]
    readonly_fields = fields 
