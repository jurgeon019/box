from django.db import models 
from tinymce.models import HTMLField
from django.shortcuts import reverse


class Page(models.Model):
  code       = models.CharField(max_length=30, blank=True, null=True, unique=True)
  meta_title = models.TextField(verbose_name=("Мета Заголовок"), blank=True, null=True)
  meta_descr = models.TextField(verbose_name=("Мета Опис"), blank=True, null=True)
  meta_key   = models.TextField(verbose_name=("Мета Ключові Слова"), blank=True, null=True)
  # url        = models.URLField(verbose_name="Урл", max_length=20, blank=True, null=True)

  class Meta:
    verbose_name="мета інформація до сторінки"
    verbose_name_plural="Мета інформація до сторінок"

  def __str__(self):
    return f'{self.meta_title}'


class PageFeature(models.Model):
  page  = models.ForeignKey(verbose_name=("Сторінка"), to='Page', related_name="features", on_delete=models.CASCADE, blank=True, null=True)
  code  = models.CharField(verbose_name=("Код"), max_length=120, null=True, blank=True, help_text=("Код, по якому контент буде діставатися у хтмл-шаблоні"))
  name  = models.CharField(verbose_name=("Назва"), max_length=120, null=True, blank=True, help_text=("Допоміжна назва"))
  value = models.TextField(verbose_name=("Текст"), null=True, blank=True, help_text=("Контент, який буде відображатися на сайті"))

  class Meta:
    verbose_name="текст сторінки"
    verbose_name_plural="Текста сторінки"
    unique_together = ('page', 'code',)

  def __str__(self):
    return f'{self.page}, {self.name}'



class PageImage(models.Model):
  page  = models.ForeignKey(verbose_name=("Сторінка"), to='Page', related_name="images", on_delete=models.CASCADE, blank=True, null=True)
  code  = models.CharField(verbose_name=("Код"), max_length=120, null=True, blank=True, help_text=("Код, по якому картинка буде діставатися у хтмл-шаблоні"))
  name  = models.CharField(verbose_name=("Назва"), max_length=120, null=True, blank=True, help_text=("Допоміжна описувальна назва"))

  class Meta:
    verbose_name="Картинки на сторінці"
    verbose_name_plural="Картинки на сторінці"
    unique_together = ('page', 'code',)

  def __str__(self):
    return f'{self.page.code}, {self.code}'

