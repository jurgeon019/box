from django.db import models 
from box.core.sw_solo.models import SingletonModel
from django.utils.translation import gettext_lazy as _

__all__ = [
  'ItemCategorySeo',
  "ItemSeo",
]

class ItemSeo(models.Model):
  categories       = models.ManyToManyField(verbose_name=_("Категорія"), to="sw_catalog.ItemCategory",  related_name='item_seos', blank=True)
  meta_title       = models.CharField(verbose_name=_("Auto Meta-title"), max_length=255, blank=True, null=True)
  meta_description = models.CharField(verbose_name=_("Auto Meta-description"), max_length=255, blank=True, null=True)
  meta_keywords    = models.CharField(verbose_name=_("Auto Meta-keywords"), max_length=255, blank=True, null=True)
  h1               = models.CharField(verbose_name=_("Auto H1"), max_length=255, blank=True, null=True)
  description      = models.TextField(verbose_name=_("Шаблон опису товарів"), blank=True, null=True)

  def __str__(self):
    return f"{self.meta_title}"
  
  def save(self, *args, **kwargs):
    # from box.apps.sw_shop.sw_catalog.models import Item 
    meta_title       = self.meta_title
    meta_description = self.meta_description
    meta_keywords    = self.meta_keywords
    description      = self.description
    categories = self.categories.all().values_list('id', flat=True)
    items = ItemCategory.objects.filter(category__in=[categories,])
    items.update(
      meta_title    = meta_title,
      meta_descr    = meta_description,
      meta_key      = meta_keywords,
      description   = description,
    )
    for item in items:
      pass
    for field in self._meta.fields:
      field = field.name
      if field != 'id':
        setattr(self, field, None)
    super().save(*args, **kwargs)

  class Meta:
    verbose_name = 'Seo Товарів'
    verbose_name_plural = 'Seo Товарів'


class ItemCategorySeo(models.Model):
  categories       = models.ManyToManyField(verbose_name=_("Категорія"), to="sw_catalog.ItemCategory",  related_name='item_category_seos', blank=True)
  meta_title       = models.CharField(verbose_name=_("Auto Meta-title"), max_length=255, blank=True, null=True)
  meta_description = models.CharField(verbose_name=_("Auto Meta-description"), max_length=255, blank=True, null=True)
  meta_keywords    = models.CharField(verbose_name=_("Auto Meta-keywords"), max_length=255, blank=True, null=True)
  h1               = models.CharField(verbose_name=_("Auto H1"), max_length=255, blank=True, null=True)
  description      = models.TextField(verbose_name=_("Шаблон опису товарів"), blank=True, null=True)

  def __str__(self):
    return f"{self.meta_title}"
  
  def save(self, *args, **kwargs):
    # from box.apps.sw_shop.sw_catalog.models import Item 
    meta_title       = self.meta_title
    meta_description = self.meta_description
    meta_keywords    = self.meta_keywords
    description      = self.description
    # print(meta_title)
    items = self.categories.all()
    items.update(
      meta_title    = meta_title,
      meta_descr    = meta_description,
      meta_key      = meta_keywords,
      description   = description,
    )
    for item in items:
      pass
    for field in self._meta.fields:
      field = field.name
      if field != 'id':
        setattr(self, field, None)
    super().save(*args, **kwargs)

  class Meta:
    verbose_name = 'Seo Товарів'
    verbose_name_plural = 'Seo Товарів'




