from django.contrib import admin 
from .models import LiqpayTransaction




class PaymentInline(admin.StackedInline):
    def has_add_permission(self, request, obj=None):
        return False 

    def has_delete_permission(self, request, obj=None):
        return False 

    # КОЛИ ЦЯ ШТУКА ВКЛЮЧЕНА - ОПЛАТИ НЕ ВІДОБРАЖАЮТЬСЯ ПІД ЗАКАЗОМ
    # def has_change_permission(self, request, obj=None):
    #     return False 
    model = LiqpayTransaction
    extra = 0
    exclude = [
        
    ]
    fields = [
        "status",
        "ip",
        "amount",
        "currency",
        "sender_phone",
        "sender_first_name",
        "sender_last_name",
        "sender_card_mask2",
        "sender_card_bank",
        "sender_card_type",
        "sender_card_country",
        "timestamp",
    ]
    readonly_fields = fields
  
    


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
    'status',
    'amount',
    'status',
    'ip',
    'order',
    'sender_phone',
    'sender_first_name',
    'sender_last_name',
    'sender_card_mask2',
    'sender_card_bank',
    'sender_card_type',
    'sender_card_country',
    ]


