from django.contrib import admin 
from shop.order.models import * 
from core.admin import custom_admin
from shop.liqpay.admin import PaymentAdmin, PaymentInline
from shop.cart.admin import CartItemInline


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
    class Meta:
        model = Order
    inlines = [
        CartItemInline,
        PaymentInline,
    ]
    list_display = [
        'id',
        'ordered',
        'name',
        'email',
        'phone',
        'address',
        # 'comments',
        'status',
        'payment_opt',
        # 'delivery_opt'
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
        # 'comments',
    ]
    list_filter = [
        'status',
        'created'
    ]
    readonly_fields = [
        'name',
        'email',
        'phone',
        'address',
        # 'comments',
        'total_price',
        # 'delivery_opt',
        'payment_opt',
        'ordered',
    ]
