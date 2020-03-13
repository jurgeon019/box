from django.db import models 
from box.solo.models import SingletonModel


__all__ = [
  'Robots',
  'ItemCategorySeo',
  "ItemSeo",
  "SeoScript",
  "Seo",
]


class Robots(SingletonModel):
  robots_txt = models.TextField(verbose_name=('robots.txt'), blank=True, null=True)

  def __str__(self):
    return f'{self.id}'

  class Meta:
    verbose_name = ('Robots.txt')
    verbose_name_plural = ('Robots.txt')


class SeoScript(models.Model):
  POSITION_CHOICES = (
    ("head_top","Після відкриваючого head"),
    ("head_bottom","Перед закриваючим head"),
    ("body_top","Після відкриваючого body"),
    ("body_bottom","Перед закриваючим body"),
  )
  setting  = models.ForeignKey(to="seo.Seo", on_delete=models.CASCADE, related_name='scripts',)
  name     = models.CharField(verbose_name=("Назва коду"), max_length=255)
  position = models.CharField(verbose_name=("Положення коду на сторінці"), max_length=255, choices=POSITION_CHOICES)
  code     = models.TextField(verbose_name=("Код для вставлення"))

  def __str__(self):
    return f'{self.name}, {self.position}, {self.code}'

  class Meta:
    verbose_name = ('Код')
    verbose_name_plural = ('Коди')


class Seo(SingletonModel):
  class Meta:
    verbose_name = ('Лічильники та коди')
    verbose_name_plural = ('Лічильники та коди')


class ItemSeo(models.Model):
  categories       = models.ManyToManyField(verbose_name=("Категорія"), to="item.ItemCategory",  related_name='item_seos', blank=True)
  meta_title       = models.CharField(verbose_name=("Auto Meta-title"), max_length=255, blank=True, null=True)
  meta_description = models.CharField(verbose_name=("Auto Meta-description"), max_length=255, blank=True, null=True)
  meta_keywords    = models.CharField(verbose_name=("Auto Meta-keywords"), max_length=255, blank=True, null=True)
  h1               = models.CharField(verbose_name=("Auto H1"), max_length=255, blank=True, null=True)
  description      = models.TextField(verbose_name=("Шаблон опису товарів"), blank=True, null=True)

  def __str__(self):
    return f"{self.meta_title}"
  
  def save(self, *args, **kwargs):
    from box.shop.item.models import Item 
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
  categories       = models.ManyToManyField(verbose_name=("Категорія"), to="item.ItemCategory",  related_name='item_category_seos', blank=True)
  meta_title       = models.CharField(verbose_name=("Auto Meta-title"), max_length=255, blank=True, null=True)
  meta_description = models.CharField(verbose_name=("Auto Meta-description"), max_length=255, blank=True, null=True)
  meta_keywords    = models.CharField(verbose_name=("Auto Meta-keywords"), max_length=255, blank=True, null=True)
  h1               = models.CharField(verbose_name=("Auto H1"), max_length=255, blank=True, null=True)
  description      = models.TextField(verbose_name=("Шаблон опису товарів"), blank=True, null=True)

  def __str__(self):
    return f"{self.meta_title}"
  
  def save(self, *args, **kwargs):
    from box.shop.item.models import Item 
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




