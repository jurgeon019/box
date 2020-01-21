from django.contrib import admin 
from core.admin import custom_admin
from shop.cart.models import Cart, CartItem, FavourItem
from django.utils.html import format_html, mark_safe
from django.urls import reverse


class CartItemInline(admin.TabularInline):
    def show_item(self, obj):
      option = "change" # "delete | history | change"
      massiv = []
      obj   = obj.item
      app   = obj._meta.app_label
      model = obj._meta.model_name
      url   = f'admin:{app}_{model}_{option}'
      href  = reverse(url, args=(obj.pk,))
      name  = f'{obj.title}'
      link  = mark_safe(f"<a href={href}>{name}</a>")
      return link
    def price_per_item(self, obj):
      return obj.price_per_item
    def total_price(self, obj):
      return obj.total_price
    def has_add_permission(self, request, obj=None):
        return False 
    def has_delete_permission(self, request, obj=None):
        return False 
    def has_change_permission(self, request, obj=None):
        return False 
    show_item.short_description      = "Товар"
    price_per_item.short_description = "Ціна за одиницю товару"
    total_price.short_description    = "Суммарна вартість товару"
    readonly_fields = [
        "show_item",
        # 'item__currency',
        'price_per_item',
        'quantity',
        'total_price',
        'ordered',
    ]
    exclude = [
      "item",
      'cart',
    ]
    model = CartItem
    extra = 0


@admin.register(Cart, site=custom_admin)
class CartAdmin(admin.ModelAdmin):
    # def has_delete_permission(self, request, obj=None):
    #     return False 
    # def has_add_permission(self, request, obj=None):
    #     return False
    def show_order(self, obj):
      option = "change" # "delete | history | change"
      massiv = []
      obj   = obj.order
      if obj:
        app   = obj._meta.app_label
        model = obj._meta.model_name
        url   = f'admin:{app}_{model}_{option}'
        args  = (obj.pk,)
        href  = reverse(url, args=args)
        name  = f'{obj.id or None}'
        name = 'order'
        link  = mark_safe(f"<a href={href}>{name}</a>")
        return link
      return '---'
    def total_price(self, obj):
        return obj.total_price
    show_order.short_description = "Замовлення"
    total_price.short_description = "Суммарна вартість корзини"
    list_display = [
        'id',
        'ordered',
        'show_order',
        'created', 
        'updated',
    ]
    list_display_links = [
      'id',
      'created',
      'updated',
    ]
    readonly_fields = [
        'total_price',
        'ordered',
        "created",
        'updated',
    ]
    fields = [ 
        'total_price',
        "ordered",
        "created",
        'updated',
    ]
    inlines = [
        # CartItemInline,
    ]


@admin.register(CartItem, site=custom_admin)
class CartItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CartItem._meta.fields]

    exclude = [
    ]
    class Meta:
        model = CartItem


# TODO: favour items
# @admin.register(FavourItem, site=custom_admin)
class FavourItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FavourItem._meta.fields]
    exclude = [
    ]
    class Meta:
        model = FavourItem