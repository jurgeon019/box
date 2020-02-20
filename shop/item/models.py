from django.core.files import File
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.utils import timezone 
from django.db import models
# from django.utils.safestring import mark_safe
from django.utils.html import mark_safe
from django.core.files.base import ContentFile
from django.conf import settings 
from django.utils.text import slugify

from transliterate import translit
import os 
from PIL import Image




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


class ItemCategoryManager(models.Manager):
	def all(self):
		return super(ItemCategoryManager, self).get_queryset().filter(is_active=True)


class ImageManager(models.Manager):
	# use_for_related_fields = True
	def all(self):
		return super(ImageManager, self).get_queryset().order_by('order')



from django.db.models.signals import pre_save



# def pre_save_item_slug(sender, instance, *args, **kwargs):
# 	if not instance.slug:
# 		slug = slugify(translit(instance.name, reversed=True))
# 		instance.slug = slug


# pre_save.connect(pre_save_item_slug, sender=Category)


class ItemStock(models.Model):
	# code = models.NullBooleanField(verbose_name=("Код"))
	text = models.CharField(verbose_name=('Наявність'), max_length=255, unique=True)

	def __str__(self):
		return f"{self.text}"
	
	class Meta:
		verbose_name = ('Наявність')
		verbose_name_plural = ('Наявність')


class ItemMarker(models.Model):
	code  = models.CharField(verbose_name=("Код"), max_length=255, unique=True) 
	text  = models.CharField(verbose_name=('Текст'), max_length=255)

	def __str__(self):
		return f"{self.text}"

	class Meta:
		verbose_name = ('Маркер')
		verbose_name_plural = ('Маркери')


class ItemManufacturer(models.Model):
	name  = models.CharField(verbose_name=('Назва'), max_length=255)

	def __str__(self):
		return f"{self.name}"
	
	class Meta:
		verbose_name = ('Виробник')
		verbose_name_plural = ('Виробники')


class ItemManager(models.Manager):

	# def get_queryset(self):
	# 	return super().get_queryset().filter(is_active=True).order_by('-order')

	def all(self):
		return super().get_queryset().filter(is_active=True).order_by('-order')

	# def get(self):
	#   return super().get_queryset().filter(is_active=True)

	# def get_queryset(self):
	#   return super().get_queryset().filter(is_active=True)



class Item(models.Model):
	objects      = ItemManager()
	# default_objects = models.Manager()

	meta_title   = models.TextField(verbose_name=("Мета заголовок"),          blank=True, null=True)
	meta_descr   = models.TextField(verbose_name=("Мета опис"),               blank=True, null=True)
	meta_key     = models.TextField(verbose_name=("Мета ключові слова"),      blank=True, null=True)

	title        = models.CharField(verbose_name=("Назва"), max_length=255, null=False)
	description  = models.TextField(verbose_name=("Опис"),                    blank=True, null=True)
	code         = models.CharField(verbose_name=("Артикул"), max_length=255,  blank=True, null=True, unique=True)   
	slug         = models.SlugField(verbose_name=("Ссилка"),  max_length=255, unique=True, blank=True, null=False)
	thumbnail    = models.ImageField(verbose_name=("Маленька картинка"), blank=True, upload_to="shop/items/thumbnails")
	markers      = models.ManyToManyField(verbose_name=("Маркери"), to='item.ItemMarker', related_name='items')
	manufacturer = models.ForeignKey(verbose_name=("Виробник"), to="item.ItemManufacturer", blank=True, null=True, on_delete=models.SET_NULL, related_name='items')

	# old_price    = models.DecimalField(verbose_name=("Стара ціна"), max_digits=10, decimal_places=2, default=0)
	# price        = models.DecimalField(verbose_name=("Нова ціна"),  max_digits=10, decimal_places=2, default=0)
	# TODO: rest_framework.serializers.ModelSerializer чогось не серіалізує DecimalField

	old_price    = models.FloatField(verbose_name=("Стара ціна"), blank=True, null=True)
	new_price    = models.FloatField(verbose_name=("Актуальна ціна"), blank=True, null=True)
	currency     = models.ForeignKey(verbose_name=("Валюта"),    to="item.Currency",     related_name="items", on_delete=models.SET_NULL, help_text=("Якщо залишити порожнім, то буде встановлена валюта категорії, у якій знаходиться товар"), blank=True, null=True)

	if settings.MULTIPLE_CATEGORY:
		categories   = models.ManyToManyField(verbose_name=("Категорія"), to='item.ItemCategory', related_name="items", blank=True, null=True)    
	else:
		category     = models.ForeignKey(verbose_name=("Категорія"), to='item.ItemCategory', related_name="items", on_delete=models.SET_NULL, blank=True, null=True)    

	in_stock     = models.ForeignKey(to="item.ItemStock", on_delete=models.CASCADE, blank=True, null=True)
	amount       = models.IntegerField(verbose_name=("Кількість"), default=1, blank=True, null=True)
	is_active    = models.BooleanField(verbose_name=("Активний"),      default=True,  help_text="Присутність товару на сайті в списку товарів")

	created      = models.DateTimeField(verbose_name=("Створений"), default=timezone.now)
	updated      = models.DateTimeField(verbose_name=("Оновлений"), auto_now_add=False, auto_now=True,  blank=True, null=True)

	order        = models.IntegerField(verbose_name=("Порядок"), default=10)

	class Meta: 
		verbose_name = ('Товар'); 
		verbose_name_plural = ('Товари')
		base_manager_name = 'objects'

	def __str__(self):
		return f"{self.slug}"

	def save(self, *args, **kwargs):
		if not self.slug:
			if self.title:
				# slug = slugify(translit(self.title, 'en', reversed=True)) 
				slug = f"{slugify(self.title)}_{self.id}"
				print(slug)
				self.slug = slug 
		self.create_currency()
		super().save(*args, **kwargs)
		if self.thumbnail:
			self.resize_thumbnail(self.thumbnail)

	def create_currency(self):
		if self.currency is None:
			print('sdf')
			if settings.MULTIPLE_CATEGORY:
				if self.categories.all():
					self.currency = self.categories.all().first().currency
				else:
					self.currency = Currency.objects.get(is_main=True)
			else:
				if self.category:
					self.currency = self.category.currency
				else:
					try:
						self.currency = Currency.objects.get(is_main=True)
					except:
						self.currency = Currency.objects.all().first()

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
		if thumbnail:
			print(thumbnail)
			self.thumbnail.save(
				thumbnail.name.split("/")[-1], 
				ContentFile(thumbnail.read()),
			)

	def get_absolute_url(self):
		return reverse("item", kwargs={"slug": self.slug})

	# def get_category(self):
	#   if self.category:
	#     category = self.category
	#   else:
	#     category = self.categories.all().first()
	#   return category

	@property
	def similars(self):
		if settings.MULTIPLE_CATEGORY:
			similars = Item.objects.filter(categories__id__in=[self.categories.all().values_list('id', flat=True)]).exclude(id=self.id)[0:50]
		else:
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
		# print('--------')
		if current_currency != main_currency:


			ratio = CurrencyRatio.objects.filter(
				main=main_currency,
				compared=current_currency,
			)
			if ratio.exists():
				# print('main_currency: ', main_currency)
				ratio = ratio.first().ratio
				price = price / ratio


			ratio = CurrencyRatio.objects.filter(
				main=current_currency,
				compared=main_currency,
			)
			if ratio.exists():
				# print('current_currency: ', current_currency)
				ratio = ratio.first().ratio
				price = price * ratio
		# print('price: ', price)
		# print('self.currency: ', self.currency)
		# print('self.price.new_price: ', self.new_price)
		# print('self.price.old_price: ', self.old_price)
		# print('__________')
		# print('\n')

		return price 

	@property
	def main_image(self):
		image = self.thumbnail
		# print(image)
		image = self.images.all().first()
		# print(image)
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
	
	def set_category(self, categories):
		if settings.MULTIPLE_CATEGORY:
			for category in categories:
				self.categories.add(category)
		else:
			self.category = categories[-1]
		self.save()


class ItemCategory(models.Model):
	meta_title = models.TextField(verbose_name=("Мета заголовок"),     blank=True, null=True)
	meta_descr = models.TextField(verbose_name=("Мета опис"),          blank=True, null=True)
	meta_key   = models.TextField(verbose_name=("Мета ключові слова"), blank=True, null=True)
	slug       = models.SlugField(verbose_name=("Посилання"),          unique=True, max_length=255)
	code       = models.CharField(verbose_name=("Код"), blank=True, null=True, max_length=255, help_text=("Код для прогера"))
	title      = models.CharField(verbose_name=("Назва"),  max_length=255,   blank=True, null=True)
	thumbnail  = models.ImageField(verbose_name=("Картинка"), blank=True, null=True, upload_to='shop/category')
	alt        = models.CharField(verbose_name=("Альт до картинки"),   blank=True, null=True, max_length=255)

	parent     = models.ForeignKey(verbose_name=("Батьківська категорія"), to='self', blank=True, null=True, on_delete=models.CASCADE, related_name='subcategories')
	currency   = models.ForeignKey(verbose_name=("Валюта"), to="item.Currency", blank=True, null=True, related_name="categories", default=1, on_delete=models.CASCADE)

	is_active  = models.BooleanField(verbose_name=("Чи активна"), default=True, help_text=("Присутність категорії на сайті"))

	created    = models.DateTimeField(verbose_name=("Створено"), default=timezone.now)
	updated    = models.DateTimeField(verbose_name=("Оновлено"), auto_now_add=False, auto_now=True, blank=True, null=True)

	# objects    = ItemCategoryManager()
	# TODO: визначити якого хуя з включеним ItemCategoryManager дочірні категорії  виводяться не ті шо треба, а всі підряд

	def save(self, *args, **kwargs): 
		if self.currency:
			try:
				self.items.all().update(currency=self.currency)
			except:
				pass
		if not self.slug:
			if self.title:
				self.slug = slugify(translit(self.title, reversed=True)) 
		super().save(*args, **kwargs)

	class Meta: 
		verbose_name = ('категорія'); 
		verbose_name_plural = ('категорії'); 
		
	def get_absolute_url(self):
		return reverse("item_category", kwargs={"slug": self.slug})
	
	@property
	def tree_title(self):
		try:
			full_path = [self.title]      
			parent = self.parent
			while parent is not None:
					# print(parent)
					full_path.append(parent.title)
					parent = parent.parent
			result = ' -> '.join(full_path[::-1]) 
		except Exception as e:
			print(e)
			result = self.title
		return result

	def __str__(self):         
		# result = f'{self.tree_title} ({self.currency})'
		result = f'{self.title}'

		return result


def item_image_folder(instance, filename):
	ext = filename.split('.')[-1]

	# foldername = instance.slug
	foldername = 'slug'

	# slug = instance.slug
	slug = 'slug'

	filename = slug + '.' + ext

	path = f"shop/items"
	path = '/'.join(['shop','items'])

	path = f"{foldername}/{filename}"
	path = '/'.join([foldername, filename])

	path = f"shop/items/{foldername}/{filename}"
	path = '/'.join(['shop', 'items', foldername, filename])

	return path 



class ItemImage(models.Model):
	item  = models.ForeignKey(verbose_name=("Товар"), to="item.Item", on_delete=models.CASCADE, related_name='images', null=True)
	image = models.ImageField(verbose_name=('Ссилка зображення'), upload_to=item_image_folder, blank=True, null=True, default='shop/items/test_item.jpg')
	alt   = models.CharField(verbose_name=("Альт"), max_length=255, blank=True, null=True)
	order = models.IntegerField(verbose_name=("Порядок"), default=1)
	# objects = ImageManager()

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


class ItemFeatureName(models.Model):
	name = models.CharField(verbose_name=("Назва характеристики"), max_length=255)

	def __str__(self):
		return f"{self.name}"
	
	class Meta:
		verbose_name = 'назва характеристики'
		verbose_name_plural = 'назви характеристики'


class ItemFeature(models.Model):
	item     = models.ForeignKey(verbose_name="Товар", to="item.Item", related_name="features", on_delete=models.CASCADE, blank=True, null=True)
	name     = models.CharField(verbose_name="Назва характеристики", max_length=255, blank=True, null=True)

	# items    = models.ManyToManyField(verbose_name=("Товар"),to='item.Item', blank=True, null=True, related_name="features")
	# name     = models.ForeignKey(to="item.ItemFeatureName",verbose_name="Назва характеристики", blank=True, null=True, related_name='features', on_delete=models.CASCADE)

	code     = models.CharField(blank=True, null=True, max_length=255, verbose_name=("Код"))
	value    = models.TextField(verbose_name="Значення характеристики", blank=True, null=True)
	category = models.ForeignKey(verbose_name="Категорія характеристики", to="item.ItemFeatureCategory", related_name="items", on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return f'{self.name}'

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
	item    = models.ForeignKey(verbose_name=("Товар"), to='item.Item', blank=True, null=True, on_delete=models.CASCADE, related_name="reviews",)
	user    = models.ForeignKey(verbose_name=("Автор"), to=User, blank=True, null=True, on_delete=models.SET_NULL, related_name="reviews",)
	text    = models.CharField(verbose_name=("Відгук"),  max_length=255, blank=True, null=True)
	phone   = models.CharField(verbose_name=("Телефон"), max_length=255, blank=True, null=True)
	name    = models.CharField(verbose_name=("Ім'я"),    max_length=255, blank=True, null=True)
	rating  = models.CharField(verbose_name=("Оцінка"), max_length=255, blank=True, null=True)
	created = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return f"{self.text}{self.rating}"

	class Meta:
		verbose_name = 'Відгук'
		verbose_name_plural = 'Відгуки'






