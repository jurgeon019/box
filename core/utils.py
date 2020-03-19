from django.utils import translation
from django.shortcuts import redirect, reverse, render 
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib import admin 
from django.db import models 
from django.utils.translation import gettext_lazy as _

from .forms import * 

from box.shop.item.models import ItemCategory 

from import_export.admin import *
from adminsortable2.admin import SortableAdminMixin
from box.custom_admin.modelclone import ClonableModelAdmin


seo = [_("SEO"), {
    "fields":[
        (
        "slug",
        "alt",
        ),
        "meta_title",
        "meta_descr",
        "meta_key",
    ],
    'classes':[
      "collapse",
    ]
}]
base_main_info = [_("ОСНОВНА ІНФОРМАЦІЯ"), {
    "fields":[
        'title',
        'image',
        'description',
    ]
}]


class AdminImageWidget(AdminFileWidget):
  def render(self, name, value, attrs=None, renderer=None):
    output = []
    if value and getattr(value, "url", None):
      image_url = value.url
      file_name = str(value)
      output.append(
        f' <a href="{image_url}" target="_blank">'
        # f'  <img src="{image_url}" alt="{file_name}" '
        # f'  <img src="{image_url}" alt="{file_name}" width="{self.width}" height="{self.height}" '
        f'  <img src="{image_url}" alt="{file_name}" width="auto" height="150" '
        f'style="object-fit: cover;"/> </a>')
    output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
    return mark_safe(''.join(output))

class BaseAdmin(
  ImportExportActionModelAdmin,
  ImportExportModelAdmin, 
  SortableAdminMixin, 
  ClonableModelAdmin, 
  admin.ModelAdmin,
  ):
    def is_active_on(self, request, queryset):
        queryset.update(is_active=True)
    def is_active_off(self, request, queryset):
        queryset.update(is_active=False)
    def show_site_link(self, obj):
        show = _("Показати на сайті")
        if obj.is_active:
          return mark_safe(f"<a href='{obj.get_absolute_url()}'>{show}</a>")
        return _(f"{obj._meta.verbose_name} не активний")
    def show_delete_link(self, obj):
        return mark_safe(f"<a href='/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.pk}/delete/' style='color:red'>x</a>")
    def show_image(self, obj):
        img  = f'<img src="{obj.image_url}" style="height:55px; max-width:150px" />'
        return mark_safe(img)
    def show_edit_link(self, obj):
        return mark_safe(f'<a href="/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.id}/change/">Змінити</a>')
    show_site_link.short_description     = ("Переглянути на сайті")
    show_edit_link.short_description   = ("Змінити")    
    show_delete_link.short_description = ("Видалити")
    show_image.short_description       = ('Зображення')
    is_active_on.short_description     = ("Увімкнути")
    is_active_off.short_description    = ("Вимкнути")
    # changelist
    actions = [
        "is_active_on",
        "is_active_off",
    ]
    list_per_page = 100
    search_fields = [
      'title',
    ]
    list_display = [
        'show_image',
        'title',
        'is_active',
        'show_site_link',
        'show_delete_link',
    ]
    list_display_links = [
        'show_image',
        'title',
    ]
    list_editable = [
        'is_active',
    ]
    list_filter = [
      'is_active',
    ]
    # changeform
    formfield_overrides = {
        models.ImageField:{'widget':AdminImageWidget}
    }
    readonly_fields = [
        'created',
        'updated',
    ]
    save_on_top = True 
    save_on_bottom = True 



def show_admin_link(obj, obj_attr=None, obj_name=None, option='change'):
  # TODO: допиляти так, шоб можна було стукатись до obj без obj_attr i obj_name
  link = '---'
  obj   = getattr(obj, obj_attr, None)
  if obj:
    name = getattr(obj, obj_name, '')
    app   = obj._meta.app_label 
    model = obj._meta.model_name 
    url = f'admin:{app}_{model}_{option}'
    href = reverse(url, args=(obj.pk,))
    link = mark_safe(f'<a href={href}>{name}</a>')
    return link 


def move_to(self, request, queryset, initial):
  form = None 
  model        = initial['model']
  attr         = initial['attr']
  message      = initial['message']
  action_value = initial['action_value']
  title        = initial['title']
  text         = initial['text']
  action_type  = initial['action_type']
  klass = queryset.first()._meta.model._meta.get_field(attr).__class__
  mro   = klass.__mro__ 
  if models.ManyToManyField in mro:
    widget = forms.CheckboxSelectMultiple
    formfield = forms.ModelMultipleChoiceField
  elif models.ForeignKey in mro:
    formfield = forms.ModelChoiceField
    widget = forms.SelectMultiple
  if 'apply' in request.POST:
    initial = {
      "model":model, 
      "formfield":formfield, 
      'widget':widget,
    }
    form = ChangeForm(data=request.POST, initial=initial)
    count = 0 
    if form.is_valid():
      field = form.cleaned_data['field']
      for item in queryset:
        klass = item._meta.model._meta.get_field(attr).__class__
        mro = klass.__mro__w
        field_type = item._meta.model._meta.get_field(attr).get_internal_type()
        # if field_type == models.ManyToManyField:
        if models.ManyToManyField in mro:
          for f in field:
            if action_type == 'remove':
              getattr(item, attr).remove(f)
            else:
              getattr(item, attr).add(f)
        # elif field_type == models.ForeignKey:
        elif models.ForeignKey in mro:
        # else:
          setattr(item, attr, field)
        item.save()
        count += 1 
      self.message_user(request, message.format(field, count))
      return redirect(request.get_full_path())
    elif not form.is_valid():
      raise("FORM IS INVALID")
  if not form:
    initial = {
        'model':model, 
        'widget':widget, 
        "formfield":formfield, 
        '_selected_action':request.POST.getlist(admin.ACTION_CHECKBOX_NAME),
      }
    form = ChangeForm(initial=initial)
    return render(request, 'core/admin/move_to.html', {
      "queryset":queryset, 
      "form":form, 
      'action_value':action_value,
      "title":title,
      'text':text,
    })


def get_sk(request):
  sk = request.session.session_key
  if not sk: 
    request.session.cycle_key()
  return sk 


def get_user(request):
  if request.user.is_anonymous:
    return None
  return request.user


def get_line():
  import inspect 
  caller = inspect.getframeinfo(inspect.stack()[1][0])
  print(caller)
  # print('filename:', inspect.getframeinfo(inspect.currentframe()).filename)
  # print('line:', inspect.getframeinfo(inspect.currentframe()).lineno)
