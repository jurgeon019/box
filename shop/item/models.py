import os 
from PIL import Image

from django.core.files import File
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.utils import timezone 
from django.db import models
# from django.utils.safestring import mark_safe
from django.utils.html import mark_safe
from django.core.files.base import ContentFile


User = get_user_model()


class Currency(models.Model):
  name    = models.CharField(verbose_name=("Назва валюти"), max_length=255)
  is_main = models.BooleanField(verbose_name=("Головна"), default=False, help_text=("Якщо валюта головна, то відносно неї будуть конвертуватись інші валюти на сайті"))

  class Meta: 
    verbose_name = ('Валюта'); 
    verbose_name_plural = ('Валюти')

  def __str__(self):
    return f"{self.name}"

  def save(self, *args, **kwargs):
    Currency.objects.all().update(is_main=False)
    super(Currency, self).save(*args, **kwargs)


class CurrencyRatio(models.Model):
  main     = models.ForeignKey(verbose_name=("Головна валюта"),     to="item.Currency", on_delete=models.CASCADE, related_name="ratio_main")
  compared = models.ForeignKey(verbose_name=("Порівнювана валюта"), to="item.Currency", on_delete=models.CASCADE, related_name="ratio_compared")
  ratio    = models.FloatField(verbose_name=("Співвідношення"), help_text=(f"Скільки одиниць порівнюваної валюти міститься в 1 одиниці головної валюти"))

  class Meta: 
    verbose_name = ('Співвідношення валют'); 
    verbose_name_plural = ('Співвідношення валют')
    unique_together = ('main','compared')

  def __str__(self):
    return f"{self.main}, {self.compared}"


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

  title       = models.CharField(verbose_name=("Назва"), max_length=255,   )
  description = models.TextField(verbose_name=("Опис"),                    blank=True, null=True)
  code        = models.CharField(verbose_name=("Артикул"), max_length=255,  blank=True, null=True)   
  slug        = models.SlugField(verbose_name=("Ссилка"),  max_length=255, unique=True)#blank=True, null=True)
  thumbnail   = models.ImageField(verbose_name=("Маленька картинка"), blank=True, upload_to="shop/items/thumbnails")

  # old_price   = models.DecimalField(verbose_name=("Стара ціна"), max_digits=10, decimal_places=2, default=0)
  # price       = models.DecimalField(verbose_name=("Нова ціна"),  max_digits=10, decimal_places=2, default=0)
  # TODO: rest_framework.serializers.ModelSerializer чогось не серіалізує DecimalField
  old_price   = models.FloatField(verbose_name=("Стара ціна"), blank=True, null=True)
  new_price   = models.FloatField(verbose_name=("Актуальна ціна"),  default=1)
  currency    = models.ForeignKey(verbose_name=("Валюта"),    to="item.Currency",     related_name="items", on_delete=models.CASCADE, help_text=("Якщо залишити порожнім, то буде встановлена валюта категорії, у якій знаходиться товар"), blank=True, null=True)
  category    = models.ForeignKey(verbose_name=("Категорія"), to='item.ItemCategory', related_name="items", on_delete=models.CASCADE, blank=True, null=True)    

  # in_stock    = models.ForeignKey(to="shop.stock", on_delete=models.CASCADE, blank=True, null=True)
  in_stock    = models.BooleanField(verbose_name=("Є в наявності"), default=True,  help_text="Мітка `Є в наявнсті` на товарі на сайті")
  is_new      = models.BooleanField(verbose_name=("Новий"),         default=False, help_text="Мітка 'New' на товарі на сайті")
  is_active   = models.BooleanField(verbose_name=("Активний"),      default=True,  help_text="Присутність товару на сайті в списку товарів")

  created     = models.DateTimeField(verbose_name=("Створений"), default=timezone.now)
  updated     = models.DateTimeField(verbose_name=("Оновлений"), auto_now_add=False, auto_now=True,  blank=True, null=True)

  objects     = ItemManager()

  class Meta: 
    verbose_name = ('Товар'); 
    verbose_name_plural = ('Товари')
    # ordering = ['-id']

  def __str__(self):
    return f"{self.slug}"
  
  def save(self, *args, **kwargs):
    self.create_currency()
    super().save(*args, **kwargs)
    if self.thumbnail:
      self.resize_thumbnail(self.thumbnail)
      print('RESIZE_THUMB')
    
  def create_currency(self):
    if self.currency is None:
      if self.category:
        self.currency = self.category.currency
      else:
        self.currency = Currency.objects.get(is_main=True)
  
  def resize_thumbnail(self, thumbnail):
    width  = 400
    img    = Image.open(thumbnail.path)
    # height = 400
    height = int((float(img.size[1])*float((width/float(img.size[0])))))
    img    = img.resize((width,height), Image.ANTIALIAS)
    img.save(thumbnail.path) 


  def create_thumbnail_from_images(self):
    thumbnail = self.images.all().first().image
    # self.thumbnail = thumbnail
    # self.save()
    self.thumbnail.save(
      thumbnail.name.split("/")[-1], 
      ContentFile(thumbnail.read()),
    )

  def get_absolute_url(self):
      return reverse("item", kwargs={"slug": self.slug})

  @property
  def similars(self):
    similars = Item.objects.filter(category=self.category).exclude(id=self.id)[0:50]
    return similars

  @property
  def is_in_stock(self):
    is_in_stock = 'Є в наявності' if self.in_stock else 'Немає в наявності'
    return is_in_stock

  @property
  def price(self):
    if self.new_price:
      price = self.new_price
    else:
      price = self.old_price
    main_currency = Currency.objects.get(is_main=True)
    current_currency = self.currency
    # current_currency = self.category.currency
    if current_currency != main_currency:
      ratio = CurrencyRatio.objects.filter(
        main=main_currency,
        compared=current_currency,
      )
      if ratio.exists():
        ratio = ratio.first().ratio
        price = price * ratio
      ratio = CurrencyRatio.objects.filter(
        main=current_currency,
        compared=main_currency,
      )
      if ratio.exists():
        ratio = ratio.first().ratio
        price = price/ratio 
    return price 

  @property
  def main_image(self):
    image = self.thumbnail
    print(image)
    image = self.images.all().first()
    print(image)
    return image

  def get_stars_total(self):
    stars_total = 0
    for review in self.reviews.all():
      stars_total += int(review.rating)
    return stars_total

  @property
  def rounded_stars(self):
    total = self.get_stars_total()
    try:
      stars = round(total/self.reviews.all().count())
    except:
      stars = 0
    return str(stars)

  @property
  def stars(self):
    total = self.get_stars_total()
    try:
      stars = total/self.reviews.all().count()
    except:
      stars = 0
    return str(stars)


class ItemCategory(models.Model):
  meta_title = models.TextField(verbose_name=("Мета заголовок"),     blank=True, null=True)
  meta_descr = models.TextField(verbose_name=("Мета опис"),          blank=True, null=True)
  meta_key   = models.TextField(verbose_name=("Мета ключові слова"), blank=True, null=True)
  slug       = models.SlugField(verbose_name=("Посилання"),          unique=True, max_length=255)
  alt        = models.CharField(verbose_name=("Альт до картинки"),   blank=True, null=True, max_length=255)

  title      = models.CharField(verbose_name=("Назва"),  max_length=255,   blank=True, null=True)
  thumbnail  = models.ImageField(verbose_name=("Картинка"), blank=True, null=True)

  parent     = models.ForeignKey(verbose_name=("Батьківська категорія"), to='self', blank=True, null=True, on_delete=models.CASCADE, related_name='subcategories')
  currency   = models.ForeignKey(verbose_name=("Валюта"), to="item.Currency", blank=True, null=True, related_name="categories", default=1, on_delete=models.CASCADE)

  is_active  = models.BooleanField(verbose_name=("Чи активна"), default=True, help_text=("Присутність категорії на сайті"))

  created    = models.DateTimeField(verbose_name=("Створено"), default=timezone.now)
  updated    = models.DateTimeField(verbose_name=("Оновлено"), auto_now_add=False, auto_now=True, blank=True, null=True)

  # objects    = ItemCategoryManager()
  # TODO: визначити якого хуя з включеним ItemCategoryManager дочірні категорії  виводяться не ті шо треба, а всі підряд


  def save(self, *args, **kwargs): 
    if self.currency:
      self.items.all().update(currency=self.currency)
    super().save(*args, **kwargs)

  class Meta: 
    verbose_name = ('Категорія товару'); 
    verbose_name_plural = ('Категорії товару'); 
    
  def get_absolute_url(self):
    return reverse("item_category", kwargs={"slug": self.slug})
  
  @property
  def tree_title(self):
    full_path = [self.title]                  
    parent = self.parent
    while parent is not None:
        full_path.append(parent.title)
        parent = parent.parent
    result = ' -> '.join(full_path[::-1]) + f' ({self.currency})'
    return result

  def __str__(self):                           
    return self.tree_title


class ItemImage(models.Model):
  item  = models.ForeignKey(verbose_name=("Товар"), to="item.Item", on_delete=models.CASCADE, related_name='images', null=True)
  image = models.ImageField(verbose_name=('Ссилка зображення'), upload_to='shop/items/', blank=True, null=True, default='shop/items/test_item.png')
  alt   = models.CharField(verbose_name=("Альт"), max_length=255, blank=True, null=True)

  def __str__(self):
    return "%s" % self.image
      
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
  name     = models.CharField(verbose_name="Назва характеристики", max_length=255, blank=True, null=True)
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


class ItemFeatureCategory(models.Model):
  parent = models.ForeignKey(verbose_name=("Батьківська категорія"), to='self',related_name='subcategories', blank=True, null=True, on_delete=models.CASCADE)
  name   = models.CharField(verbose_name=("Назва категорії"), max_length=255, unique=True, blank=True, null=True)
  
  def __str__(self):
    return f"{self.name}"

  class Meta:
    verbose_name = 'Категорія характеристики'
    verbose_name_plural = 'Категорії характеристики'


class ItemReview(models.Model):
  item    = models.ForeignKey(verbose_name=("Батьківська категорія"), to='item.Item', blank=True, null=True, on_delete=models.CASCADE, related_name="reviews",)
  user    = models.ForeignKey(verbose_name=("Автор"), to=User, blank=True, null=True, on_delete=models.SET_NULL, related_name="reviews",)
  text    = models.CharField(verbose_name=("Відгук"),  max_length=255, blank=True, null=True)
  phone   = models.CharField(verbose_name=("Телефон"), max_length=255, blank=True, null=True)
  name    = models.CharField(verbose_name=("Ім'я"),    max_length=255, blank=True, null=True)
  rating  = models.CharField(verbose_name=("Рейтинг"), max_length=255, blank=True, null=True)
  created = models.DateTimeField(default = timezone.now)

  def __str__(self):
    return f"{self.text}{self.rating}"

  class Meta:
    verbose_name = 'Відгук'
    verbose_name_plural = 'Відгуки'


