from django.utils.translation import gettext_lazy as _
from django.contrib import admin 
from django.shortcuts import reverse, render, redirect
from django.utils.html import mark_safe

from box.apps.sw_shop.order.models import Order, Status
# from box.apps.sw_payment.liqpay.admin import PaymentInline
from box.apps.sw_shop.cart.admin import CartItemInline
from box.core.utils import show_admin_link
from box.core.sw_solo.admin import SingletonModelAdmin

from ..models import *
from ..filters import * 
from ..forms import * 

from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline, TranslationTabularInline


class OrderInline(admin.TabularInline):
    def show_link(self, obj):
        return mark_safe(f'<a href="/admin/order/order/{obj.id}/change">Замовлення № {obj.id}</a>')
    show_link.short_description = _("Ссилка")
    model = Order 
    extra = 0
    fields = [
        'show_link',
        'name',
        'email',
        'phone',
        'address',
        'total_price',
        'paid',
        'ordered',
        'created',
    ]
    readonly_fields = [
        'show_link'
    ]
    
    def has_change_permission(self, request, obj):
        return False
    def has_delete_permission(self, request, obj):
        return False
    def has_add_permission(self, request, obj):
        return False


class StatusAdmin(TabbedTranslationAdmin):
  def get_model_perms(self, request):
    return {}
  search_fields = [
    'name'
  ]


class OrderTagAdmin(TabbedTranslationAdmin):
  def get_model_perms(self, request):
    return {}
  # model_perms = {}
  search_fields = [
    'name'
  ]


from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter




class OrderAdmin(admin.ModelAdmin):
    def total_with_coupon(self, obj=None):
        return f'{obj.total_price_with_coupon} {obj.currency}'
    def total_without_coupon(self, obj=None):
        return f'{obj.total_price_with_coupon} {obj.currency}'
    def show_user(self, obj):
      link = show_admin_link(obj, obj_attr='user', obj_name='username', option='change')
      return link
    def show_id(self, obj):
      return mark_safe(f'<a href="/admin/order/order/{obj.id}/change" >Замовлення № {obj.id}</a>')
    def items_count(self, obj):
      return obj.cart_items.all().count()
    def delete(self, obj):
      return mark_safe(f'<a href="/admin/order/order/{obj.id}/delete" style="color:red" >x</a>')
    def change_status(self, request, queryset):
      form = None 
      if 'apply' in request.POST:
        form = ChangeStatusForm(request.POST)
        if form.is_valid():
          status = form.cleaned_data['status']
          count = 0 
          for item in queryset:
            item.status = status 
            item.save()
            count += 1 
        self.message_user(request, f'Статус {status} був застосований для {count} товарів')
        return redirect(request.get_full_path())
      if not form:
          form = ChangeStatusForm(initial={"_selected_action":request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
          return render(request, 'order/admin/change_status.html', {'items':queryset, 'form':form, 'title':'Зміна статусу'})
    def put_tags_on(self, request, queryset):
      form = None 
      print(request.POST)
      if 'apply' in request.POST:
        form = ChangeTagsForm(request.POST)
        if form.is_valid():
          tags = form.cleaned_data['tags']
          count = 0 
          for item in queryset:
            for tag in tags:
              item.tags.add(tag)
              item.save()
              count+=1
        self.message_user(request, f'Теги {tags} були додані до {count} товарів')
        return redirect(request.get_full_path())
      if not form:
        form = ChangeTagsForm(initial={'_selected_action':request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        return render(request, 'order/admin/change_tags.html', {
          'items':queryset, 'form':form, 'title':'Зміна тегів',
          'value':'put_tags_on',
          'text':'Новый тег будет назначен для следующих позиций'
          })
    def put_tags_off(self, request, queryset):
      form = None 
      print(request.POST)
      if 'apply' in request.POST:
        form = ChangeTagsForm(request.POST)
        if form.is_valid():
          tags = form.cleaned_data['tags']
          count = 0 
          for item in queryset:
            for tag in tags:
              item.tags.remove(tag)
              item.save()
              count+=1
        self.message_user(request, f'Теги {tags} були забрані з {count} товарів')
        return redirect(request.get_full_path())
      if not form:
        form = ChangeTagsForm(initial={'_selected_action':request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        return render(request, 'order/admin/change_tags.html', {
          'items':queryset, 'form':form, 'title':'Зміна тегів',
          'value':'put_tags_off',
          'text':'Теги будуть забрані з наступних позицій'
        })
    def show_tags(self, obj):
      result = ''
      for tag in obj.tags.all():
        result += (f'<span style="background-color:{tag.color}">{tag.name}</span><br>')
      if not result:
        return '---'
      return mark_safe(result)
    show_tags.short_description = ("Теги")
    
    actions = [
      change_status,
      put_tags_on,
      put_tags_off,
    ]
    date_hierarchy = 'created'
    show_user.short_description = _('Користувач')
    show_id.short_description = _('ID замовлення')
    items_count.short_description = _('Товари')
    
    total_with_coupon.short_description = _('Сумма замовлення без скидкою')
    total_without_coupon.short_description = _('Сумма замовлення зі скидкою')
    inlines = [
        CartItemInline,
        # PaymentInline,
    ]
    list_display = [
        'show_id',
        'name',
        'status',
        'show_tags',
        'items_count',
        'total_price',
        'created',
        'delete',
    ]
    list_display_links = [
      'show_id',
      'name',
      'items_count',
      'total_price',
      'created',
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
        'note',
    ]
    list_filter = [
        'status',
        'tags',
        ('created', DateTimeRangeFilter), 
        ('updated', DateTimeRangeFilter),
    ]
    fields = [
        # 'user',
        'show_user',
        'status',
        'tags',
        'name',
        'email',
        'phone',
        'address',
        'comments',
        'coupon',
        'payment_opt',
        'delivery_opt',
        'ordered',
        'paid',
        "total_with_coupon",
        "total_without_coupon",
        'note',
    ]
    autocomplete_fields = [ 
      'status',
      'tags',
      'coupon',
    ]
    readonly_fields = [
        'show_user',
        'total_with_coupon',
        'total_without_coupon',
    ]
    list_per_page = 100 



class ItemRequestAdmin(admin.ModelAdmin):
    def show_item(self, obj=None):
        from django.shortcuts import reverse 
        from django.utils.html import mark_safe 
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

    show_item.short_description = _('Товар')
    readonly_fields = [
        'show_item',
        'name',
        'email',
        'phone',
        'message',
    ]
    fields = [
        'show_item',
        'name',
        'email',
        'phone',
        'message',
    ]


class OrderTagInline(TranslationTabularInline):
    extra = 0 
    model = OrderTag
     

class StatusInline(TranslationTabularInline):
    extra = 0 
    model = Status
     

class OrderConfigAdmin(SingletonModelAdmin):
  inlines = [
    OrderTagInline, 
    StatusInline
  ]


