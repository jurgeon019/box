from django.contrib import admin 
from box.shop.order.models import * 
from box.admin import custom_admin
from box.shop.liqpay.admin import PaymentAdmin, PaymentInline
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


@admin.register(Status, site=custom_admin)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Order, site=custom_admin)
class OrderAdmin(admin.ModelAdmin):
    def total(self, obj=None):
        return f'{obj.total_price} {obj.currency}'

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
        'payment_opt',
        'ordered',
        'status',
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
    exclude = [
        'sk', 
        'user',
        'comments',
        'delivery_opt',
        
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
        'created'
    ]
    fields = [
        'name',
        'email',
        'phone',
        'address',
        'payment_opt',
        'ordered',
        'total',
    ]
    readonly_fields = [
        'name',
        'email',
        'phone',
        'address',
        'payment_opt',
        'ordered',
        'total',

    ]


