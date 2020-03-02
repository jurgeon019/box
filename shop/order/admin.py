from django.contrib import admin 
from django.shortcuts import reverse 
from django.utils.html import mark_safe



from box.shop.order.models import Order, Status
from box.shop.liqpay.admin import PaymentInline
from box.shop.cart.admin import CartItemInline




class OrderInline(admin.TabularInline):
    model = Order 
    extra = 0
    fields = [
        'name',
        'email',
        'phone',
        'address',
        'created',
    ]
    readonly_fields = [
        'created'
    ]
    def has_change_permission(self, request, obj):
        return False
    def has_delete_permission(self, request, obj):
        return False
    def has_add_permission(self, request, obj):
        return False


class StatusAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    def total(self, obj=None):
        return f'{obj.total_price} {obj.currency}'
    def show_user(self, obj):
      option = "change" # "delete | history | change"
      massiv = []
      obj   = obj.user
      app   = obj._meta.app_label
      model = obj._meta.model_name
      url   = f'admin:custom_auth_{model}_{option}'
      href  = reverse(url, args=(obj.pk,))
      name  = f'{obj.username}'
      link  = mark_safe(f"<a href={href}>{name}</a>")
      return link
    show_user.short_description = 'Користувач'

    total.short_description = 'Сумма замовлення'
    inlines = [
        CartItemInline,
        PaymentInline,
    ]
    list_display = [
        'id',
        'name',
        'email',
        'phone',
        'address',
        'status',
        'ordered',
        'payment_opt',
    ]
    list_display_links = [
        'name',
        'email',
        'phone',
        'address',
        'payment_opt',
    ]
    list_editable = [
        'status'
    ]
    search_fields = [
        'user__username',
        'name',
        'email',
        'phone',
        'address',

    ]
    list_filter = [
        'status',
        'created',
        'updated',
    ]
    fields = [
        # 'user',
        'show_user',
        'name',
        'email',
        'phone',
        'address',
        'comments',
        'payment_opt',
        'delivery_opt',
        'ordered',
        'total',
        'status',
    ]
    readonly_fields = [
        # 'user',
        'show_user',
        'name',
        'email',
        'phone',
        'address',
        'comments',
        'payment_opt',
        'delivery_opt',
        'ordered',
        'total',
    ]



