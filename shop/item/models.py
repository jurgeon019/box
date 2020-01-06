from PIL import Image

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.utils import timezone 
from django.db import models
from django.utils.safestring import mark_safe


from shop.item.utils import get_family_tree


User = get_user_model()


STOCK_CHOICES = (
  ("Є в наявності","Є в наявності"),
  ("Немає в наявності","Немає в наявності"),
  ("Немає на складі","Немає на складі"),
  ("Очікується поставка", "Очікується поставка"),
)

RATING_CHOICES = (
  (1, 1),
  (2, 2),
  (3, 3),
  (4, 4),
  (5, 5),
)


class ItemManager(models.Manager):
  def all(self):
    return super(ItemManager, self).get_queryset().filter(is_active=True)

class ItemCategoryManager(models.Manager):
  def all(self):
    return super(ItemCategoryManager, self).get_queryset().filter(is_active=True)


class Item(models.Model):
  meta_title  = models.TextField(verbose_name=("Мета заголовок"),          blank=True, null=True)
  meta_descr  = models.TextField(verbose_name=("Мета опис"),               blank=True, null=True)
  meta_key    = models.TextField(verbose_name=("Мета ключові слова"),      blank=True, null=True)

  title       = models.CharField(verbose_name=("Назва"), max_length=120,   blank=True, null=True)
  description = models.TextField(verbose_name=("Опис"),                    blank=True, null=True)
  code        = models.CharField(verbose_name=("Артикул"), max_length=20,  blank=True, null=True)   
  slug        = models.SlugField(verbose_name=("Ссилка"),  max_length=255, unique=True)#blank=True, null=True)

  # old_price   = models.DecimalField(verbose_name=("Стара ціна"), blank=True, null=True, max_digits=10, decimal_places=2, default=0)
  # price       = models.DecimalField(verbose_name=("Нова ціна"),  blank=True, null=True, max_digits=10, decimal_places=2, default=0)
  old_price   = models.FloatField(verbose_name=("Стара ціна"), blank=True, null=True, default=1)
  new_price   = models.FloatField(verbose_name=("Нова ціна"),  blank=True, null=True, default=1)
  # currency    = models.CharField(verbose_name=("Валюта"),      blank=True, null=True, max_length=120, default='грн')

  category    = models.ForeignKey(verbose_name=("Категорія"), to='item.ItemCategory', related_name="items", on_delete=models.CASCADE, blank=True, null=True, help_text=' ')    

  # in_stock    = models.CharField(max_length=120, blank=True, null=True, choices=STOCK_CHOICES)
  # in_stock    = models.ForeignKey(to="shop.stock", on_delete=models.CASCADE, blank=True, null=True)
  in_stock    = models.BooleanField(verbose_name=("Є в наявності"), default=True,  help_text="Мітка `Є в наявнсті` на товарі на сайті")
  is_new      = models.BooleanField(verbose_name=("Новий"),         default=False, help_text="Мітка 'New' на товарі на сайті")
  is_active   = models.BooleanField(verbose_name=("Активний"),      default=True,  help_text="Присутність товару на сайті в списку товарів")

  created     = models.DateTimeField(verbose_name=("Створений"), auto_now_add=True,  auto_now=False, blank=True, null=True)
  updated     = models.DateTimeField(verbose_name=("Оновлений"), auto_now_add=False, auto_now=True,  blank=True, null=True)

  objects     = ItemManager()

  class Meta: 
    verbose_name = ('Товар'); 
    verbose_name_plural = ('Товари')
    # ordering = ['-id']

  def __str__(self):
    return f"{self.slug}"
  
  def currency(self):
    currency = 'грн'
    if self.category:
      currency = self.category.currency
    return currency

  def get_absolute_url(self):
      return reverse("item", kwargs={"slug": self.slug})

  @property
  def similars(self):
    similars = Item.objects.filter(category=self.category).all()[0:50]
    return similars

  @property
  def is_in_stock(self):
    is_in_stock = 'Є в наявності' if self.in_stock else 'Немає в наявності'
    return is_in_stock

  @property
  def price(self):
    if self.new_price:
      return self.new_price
    else:
      return self.old_price

  @property
  def main_image(self):
    return self.images.all().first()


class ItemCategory(models.Model):
  meta_title = models.TextField(verbose_name=("Мета заголовок"),     blank=True, null=True)
  meta_descr = models.TextField(verbose_name=("Мета опис"),          blank=True, null=True)
  meta_key   = models.TextField(verbose_name=("Мета ключові слова"), blank=True, null=True)
  title      = models.CharField(verbose_name=("Назва"),  max_length=120,   blank=True, null=True)
  currency   = models.CharField(verbose_name=("Валюта"), max_length=120,   blank=True, null=True)
  # code       = models.CharField(verbose_name=("Код"),                blank=True, null=True, unique=True, max_length=20)
  slug       = models.SlugField(verbose_name=("Посилання"),         unique=True, max_length=255)
  # is_main    = models.BooleanField(verbose_name=("Головна"),         default=False)
  is_active  = models.BooleanField(verbose_name=("Чи активна"),         default=True, help_text=("Присутність категорії на сайті в списку категорій"))
  parent     = models.ForeignKey(verbose_name=("Батьківська категорія"), to='self', blank=True, null=True, on_delete=models.CASCADE, related_name='subcategories')
  created    = models.DateTimeField(verbose_name=("Створено"), default=timezone.now)#auto_now_add=True, auto_now=False, blank=True, null=True)
  updated    = models.DateTimeField(verbose_name=("Оновлено"), auto_now_add=False, auto_now=True, blank=True, null=True)
  # objects    = ItemCategoryManager()
  # TODO: визначити якого хуя з включеним ItemCategoryManager дочірні категорії  виводяться не ті шо треба, а всі підряді

  currency   = models.CharField(verbose_name=("Валюта категорії"), max_length=255, blank=True, null=True, default='грн.')
  def __str__(self): 
    return f'{self.title}'

  class Meta: 
    verbose_name = 'Категорія товару'; 
    verbose_name_plural = 'Категорії товару'; 
    
  def get_absolute_url(self):
    return reverse("item_category", kwargs={"slug": self.slug})
  
  @property
  def tree_title(self):
    full_path = [self.title]                  
    parent = self.parent
    while parent is not None:
        full_path.append(parent.title)
        parent = parent.parent
    return ' -> '.join(full_path[::-1])

  def __str__(self):                           
    return self.tree_title


class ItemImage(models.Model):
  item  = models.ForeignKey(to="item.Item", on_delete=models.CASCADE, related_name='images')
  image = models.ImageField(verbose_name=('Ссилка зображення'), upload_to='shop/items/', blank=True, null=True, default='shop/items/test_item.png')
  alt   = models.CharField(max_length=120, blank=True, null=True)

  def __str__(self):
    return "%s" % self.image.url
      
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    # img = Image.open(self.image.path)
    # img = img.resize((400, 400), Image.ANTIALIAS)
    # img.save(self.image.path)

  class Meta: 
    verbose_name = ('Зображення товару'); 
    verbose_name_plural = ('Зображення товару'); 


class ItemFeature(models.Model):
  item     = models.ForeignKey(verbose_name="Товар", to="item.Item", related_name="features", on_delete=models.CASCADE, blank=True, null=True)
  # items    = models.ManyToManyField(verbose_name=("Товар"),to='item.Item', blank=True, null=True, related_name="features")
  name     = models.CharField(verbose_name="Назва характеристики", max_length=120, blank=True, null=True)
  # name     = models.ForeignKey(to="shop.FeatureName",verbose_name="Назва характеристики", blank=True, null=True, on_delete=models.CASCADE)
  code     = models.CharField(blank=True, null=True, max_length=255, verbose_name=("Код"))
  value    = models.TextField(verbose_name="Значення характеристики", blank=True, null=True)
  category = models.ForeignKey(verbose_name="Категорія характеристики", to="item.ItemFeatureCategory", related_name="items", on_delete=models.CASCADE, blank=True, null=True)

  def __str__(self):
    return f"{self.item}, {self.code}, {self.name}"
    # return f"{self.items.all()}, {self.code}, {self.name}"

  class Meta:
    verbose_name = 'Характеристика товару'
    verbose_name_plural = 'Характеристики товару'
    # unique_together = 


# class FeatureName(models.Model):
#   name     = models.CharField(verbose_name="Назва характеристики", max_length=120, blank=True, null=True)


class ItemFeatureCategory(models.Model):
  parent = models.ForeignKey(verbose_name=("Батьківська категорія"), to='self',related_name='subcategories', blank=True, null=True, on_delete=models.CASCADE)
  name   = models.CharField(verbose_name=("Назва категорії"), max_length=120, unique=True, blank=True, null=True)
  
  def __str__(self):
    return f"{self.name}"

  class Meta:
    verbose_name = 'Категорія характеристики'
    verbose_name_plural = 'Категорії характеристики'


class ItemReview(models.Model):
  item    = models.ForeignKey(verbose_name=("Батьківська категорія"), to='item.Item', blank=True, null=True, on_delete=models.CASCADE, related_name="reviews",)
  text    = models.CharField(verbose_name=("Відгук"), max_length=120, blank=True, null=True)
  phone    = models.CharField(verbose_name=("Телефон"), max_length=120, blank=True, null=True)
  user    = models.ForeignKey(verbose_name=("Автор"), to=User, blank=True, null=True, on_delete=models.SET_NULL, related_name="reviews",)
  name    = models.CharField(verbose_name=("Ім'я"), max_length=120, blank=True, null=True)
  rating  = models.IntegerField(verbose_name=("Рейтинг"), blank=True, null=True, choices=RATING_CHOICES)
  created = models.DateTimeField(default = timezone.now)

  def __str__(self):
    return f"{self.text}"

  class Meta:
    verbose_name = 'Відгук'
    verbose_name_plural = 'Відгуки'

