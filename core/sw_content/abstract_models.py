from django.db import models 
from django.utils.translation import gettext_lazy as _
from django.utils import timezone 

from box.core.helpers import get_admin_url
from box.core.models import BaseMixin

# class AbstractContent(models.Model):
  # code    = models.SlugField(
  #   verbose_name=_("Змінна"), max_length=255,
  #   unique=True, null=False, blank=False, 
  #   help_text=("Назва змінної, по якій об'єкт буде діставатись у HTML-шаблоні."), 
  # )
  # created = models.DateTimeField(
  #   verbose_name=_("Створено"), default=timezone.now, blank=True, null=True)
  # updated = models.DateTimeField(verbose_name=_("Оновлено"), auto_now=True,auto_now_add=False)
  # def get_admin_url(self):
  #   return get_admin_url(self)
  # @classmethod
  # def modeltranslation_fields(self):
  #   return []

class AbstractContent(BaseMixin):

  page    = models.ForeignKey(
    verbose_name=_("Сторінка"), to="sw_content.Page", 
    on_delete=models.SET_NULL, blank=True, null=True,
  )

  class Meta:
    abstract = True 
    ordering = [
      '-updated',
    ]

  def __str__(self):
    return f'{self.page}, {self.code}'

  def save(self, *args, **kwargs):
    if not self.page:
      from .models import Page 
      page = Page.objects.get_or_create(code='general')[0]
      page.meta_title = _('Загальна сторінка')
      page.save()
      self.page = page
    super().save(*args, **kwargs)


class AbstractText(AbstractContent):
  text  = models.TextField(
    verbose_name=_("Текст"), 
    null=False, blank=False, 
  )

  @property
  def get_text(self):
    text = ''
    if self.text:
      text = self.text 
    return text 

  @classmethod
  def modeltranslation_fields(cls):
    fields = [
      'text',
    ]
    return fields

  class Meta:
    abstract = True 


class AbstractLink(AbstractText):
  href = models.CharField(
    verbose_name=_("Посилання"), max_length=255,
    blank=False, null=False,
  )
  class Meta:
      abstract = True 

