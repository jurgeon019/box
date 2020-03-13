from django.db import models 


class Page(models.Model):
  code       = models.CharField(verbose_name=("Код"), max_length=30, blank=False, null=False, unique=True)
  meta_title = models.CharField(verbose_name=("Заголовок"), max_length=255, blank=True, null=True)
  meta_descr = models.TextField(verbose_name=("Опис"), blank=True, null=True)
  meta_key   = models.TextField(verbose_name=("Ключові слова"), blank=True, null=True)
  # slug        = models.URLField(verbose_name="Урл", max_length=255, blank=True, null=True)
  slug        = models.SlugField(verbose_name="Урл", max_length=255, blank=True, null=True)
  
  class Meta:
    verbose_name="Сторінка"
    verbose_name_plural="Сторінки"

  def __str__(self):
    return f'{self.code}, {self.meta_title}'
    
  @classmethod
  def modeltranslation_fields(cls):
    fields = [
        'meta_title',
        'meta_descr',
        'meta_key',    
      ]
    return fields

from tinymce import HTMLField

class PageFeature(models.Model):
  page  = models.ForeignKey(verbose_name=("Сторінка"), to='page.Page', related_name="features", on_delete=models.SET_NULL, blank=True, null=True)
  code  = models.CharField(verbose_name=("Змінна"), max_length=255, null=False, blank=False, help_text=("Назва змінної, що використовується в шаблоні."), unique=True)
  value = HTMLField(verbose_name=("Текст"), null=True, blank=True, help_text=("Контент, який буде відображатися на сайті"))

  class Meta:
    verbose_name="переклад"
    verbose_name_plural="переклади"

  def __str__(self):
    return f'{self.page}, {self.code}'

  @classmethod
  def modeltranslation_fields(cls):
    fields = [
      'value',
    ]
    return fields


class PageImage(models.Model):
  # TODO: переробити на generic, чи на шо там ше 
  code  = models.CharField(verbose_name=("Код"), max_length=120, null=True, blank=True, help_text=("Код, по якому картинка буде діставатися у хтмл-шаблоні"))
  value = models.ImageField(verbose_name=("Картинка"), upload_to="pages/", null=True, blank=True, help_text=("Картинка, яка буде відображатися на сайті"))
  page  = models.ForeignKey(verbose_name=("Сторінка"), to='page.Page', related_name="images", on_delete=models.SET_NULL, blank=True, null=True)

  class Meta:
    verbose_name="Картинка на сторінці"
    verbose_name_plural="Картинки на сторінці"

  def __str__(self):
    return f'{self.page.code}, {self.code}'


