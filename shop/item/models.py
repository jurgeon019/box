from django.db import models 
from django.contrib import admin 
from django.core.files import File
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.db import models
from django.utils.html import mark_safe
from django.core.files.base import ContentFile
from django.conf import settings 
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.db.models.signals import post_save, pre_save

from tinymce import HTMLField
from transliterate import translit, get_available_language_codes#, slugify
from transliterate import translit
from adminsortable.fields import SortableForeignKey
from mptt.models import MPTTModel, TreeForeignKey
from adminsortable.admin import SortableAdmin, NonSortableParentAdmin, SortableStackedInline
from adminsortable.fields import SortableForeignKey
import os 
from PIL import Image

from box.core.managers import *
from box.core.models import AbstractPage, BaseMixin
from .utils import generate_unique_slug, item_image_folder




__all__ = [
	"Item",
	"ItemCurrency",
	"ItemCurrencyRatio",
	"ItemStock",
	"ItemMarker",
	"ItemManufacturer",
	"ItemCategory",
	"ItemBrand",
	"ItemImage",
	'ItemOption',
	"ItemFeature",
	"ItemFeatureName",
	"ItemFeatureValue",
	"ItemFeatureCategory",
	"ItemReview",
	"ItemVariant",
]


User = get_user_model()


STOCK_COLOR_CHOICES = (
	('g', "green"),
	('o', "orange"),
	('r', "red"),
)


class Item(AbstractPage):
	if settings.MULTIPLE_CATEGORY:
		categories   = models.ManyToManyField(verbose_name=_("Категорія"), to='item.ItemCategory', related_name="items", blank=True)    
	else:
		category     = TreeForeignKey(verbose_name=_("Категорія"), to='item.ItemCategory', related_name="items", on_delete=models.SET_NULL, blank=True, null=True)    
	markers      = models.ManyToManyField(verbose_name=_("Маркери"), to='item.ItemMarker', related_name='items', blank=True)
	similars     = models.ManyToManyField(verbose_name=_("Схожі товари"), to="self", related_name="similars_set", blank=True, default=None)
	manufacturer = models.ForeignKey(verbose_name=_("Виробник"), to="item.ItemManufacturer", blank=True, null=True, on_delete=models.SET_NULL, related_name='items')
	brand        = models.ForeignKey(verbose_name=_("Бренд"), to='item.ItemBrand', related_name='items', on_delete=models.SET_NULL, null=True, blank=True)
	in_stock     = models.ForeignKey(verbose_name=_("Наявність"), to="item.ItemStock", on_delete=models.SET_NULL, blank=True, null=True, help_text='"Кількість" в пріорітеті над "наявністю"')
	currency     = models.ForeignKey(verbose_name=_("Валюта"),    to="item.ItemCurrency",     related_name="items", on_delete=models.SET_NULL, help_text=("Якщо залишити порожнім, то буде встановлена валюта категорії, у якій знаходиться товар"), blank=True, null=True)
	# old_price    = models.DecimalField(verbose_name=_("Стара ціна"), max_digits=10, decimal_places=2, default=0)
	# price        = models.DecimalField(verbose_name=_("Нова ціна"),  max_digits=10, decimal_places=2, default=0)
	# TODO: rest_framework.serializers.ModelSerializer чогось не серіалізує DecimalField
	old_price    = models.FloatField(verbose_name=_("Стара ціна"), blank=True, null=True)
	new_price    = models.FloatField(verbose_name=_("Актуальна ціна"), blank=True, null=True)
	units         = models.CharField(verbose_name=_("Одиниці вимірювання"), blank=True, null=True, max_length=255)
	amount       = models.PositiveIntegerField(verbose_name=_("Кількість"), blank=True, null=True, default=None, help_text='"Кількість" в пріорітеті над "наявністю"')

	class Meta: 
		verbose_name = _('Товар'); 
		verbose_name_plural = _('Товари')
		ordering = ['order']

	def __str__(self):
		return f"{self.title}, {self.slug}"

	def save(self, *args, **kwargs):
		# self.handle_currency(*args, **kwargs)
		# self.handle_category(*args, **kwargs) #TODO:
		self.handle_slug(*args, **kwargs)
		self.handle_availability(*args, **kwargs)
		super().save(*args, **kwargs)
		self.resize_image(self.image)

	def handle_slug(self, *args, **kwargs):
		if not self.slug:
			from transliterate.exceptions import LanguagePackNotFound, LanguageDetectionError
			try:
				slug = slugify(translit(self.title, reversed=True)) 
			except Exception as e:
				slug = f"{slugify(self.title)}"

			origin_slug = slug
			numb = 1
			while Item.objects.filter(slug=slug).exists():
				slug = f'{origin_slug}-{numb}'
				numb += 1
			self.slug = slug

	def handle_availability(self, *args, **kwargs):
		'''
		self.in_stock              == None  - безкінечний
		self.in_stock.availability == False - відсутній
		self.in_stock.availability == True  - присутній 

		self.amount == None                 - безкінечний
		self.amount == 0                    - відсутній
		self.amount > 0                     - присутній 

		'''

		available_stocks   = ItemStock.objects.filter(availability=True)
		unavailable_stocks = ItemStock.objects.filter(availability=False)

		if self.amount == 0:
			if unavailable_stocks.exists():
				self.in_stock = unavailable_stocks.first()
		# if self.amount == None or self.amount > 0:
		# 	if available_stocks.exists():
		# 		self.in_stock = available_stocks.first()
		# 	else:
		# 		self.in_stock == None 
		 
	def handle_currency(self, *args, **kwargs):
		if not self.currency:
			if settings.MULTIPLE_CATEGORY:
				if self.categories.all().exists():
					self.currency = self.categories.all().first().currency
				else:
					try:
						self.currency = ItemCurrency.objects.get(is_main=True)
					except:
						self.currency = ItemCurrency.objects.all().first()
			else:
				if self.category:
					self.currency = self.category.currency
				else:
					try:
						self.currency = ItemCurrency.objects.get(is_main=True)
					except:
						self.currency = ItemCurrency.objects.all().first()

	def resize_image(self, image):
		if image:
			width  = 400
			img    = Image.open(image.path)
			# height = 400
			height = int((float(img.size[1])*float((width/float(img.size[0])))))
			img    = img.resize((width,height), Image.ANTIALIAS)
			img.save(image.path) 

	def create_image_from_images(self):
		image = self.images.all().first().image
		# self.image = image
		# self.save()
		if image:
			# print(image)
			self.image.save(
				image.name.split("/")[-1], 
				ContentFile(image.read()),
			)

	def get_absolute_url(self):
		return reverse("item", kwargs={"slug": self.slug})

	@property
	def is_in_stock(self):
		if self.amount == 0:
			is_in_stock = False
		else:
			is_in_stock = True 
		return is_in_stock
	
	def main_img(self):
		return ItemImage.objects.filter(item=self).first()

	@property
	def price(self):
		if self.new_price:
			price = self.new_price
		elif self.old_price:
			price = self.old_price
		else:
			return 0
		
		# return price 
		# !!!!!!!!!!!!
		main_currency = ItemCurrency.objects.get(is_main=True)
		current_currency = self.currency
		# current_currency = self.category.currency
		# print('--------')
		if current_currency != main_currency:


			ratio = ItemCurrencyRatio.objects.filter(
				main=main_currency,
				compared=current_currency,
			)
			if ratio.exists():
				# print('main_currency: ', main_currency)
				ratio = ratio.first().ratio
				# print('\n')
				price = price / ratio


			ratio = ItemCurrencyRatio.objects.filter(
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
		print(price)
		return price 

	@property
	def main_image(self):
		image = self.image
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

	def get_categories(self, ):

		return categories 
	
	def in_cart(self, request):
		from box.shop.cart.models import CartItem
		from box.shop.cart.utils import get_cart
		in_cart = self.id in CartItem.objects.filter(cart=get_cart(request)).values_list('item__id', flat=True)
		return in_cart 


class ItemBrand(AbstractPage):
	def get_absolute_url(self):
		try:
			return reverse("brand", kwargs={"slug": self.slug})
		except:
			return '' 
	class Meta:
		verbose_name = _('Бренд')
		verbose_name_plural = _("Бренди")
		ordering = ['order']


class ItemCategory(AbstractPage, MPTTModel):
	# TODO: визначити якого хуя з включеним ItemCategoryManager дочірні категорії  виводяться не ті шо треба, а всі підряд
	parent     = TreeForeignKey(verbose_name=_("Батьківська категорія"), to='self', blank=True, null=True, on_delete=models.SET_NULL, related_name='subcategories')
	currency   = models.ForeignKey(verbose_name=_("Валюта"), to="item.ItemCurrency", blank=True, null=True, related_name="categories",  on_delete=models.SET_NULL)

	class Meta: 
		verbose_name = _('категорія'); 
		verbose_name_plural = _('категорії'); 
		unique_together = ('title', 'parent')
		ordering = ['order']
	
	def get_absolute_url(self):
		return reverse("item_category", kwargs={"slug": self.slug})

	@property
	def parent_slug(self):
		slug = ''
		if self.parent:
			slug = self.parent.slug	
		return slug
	
	@property
	def parents(self):
		parent = self.parent 
		parents = [self, parent]
		# parents = [parent]
		if parent:
			while parent.parent:
				parent = parent.parent 
				parents.append(parent)
				# parents.insert(0, parent)
		# parents = reversed(parents)
		return parents[-1::-1]

	@property
	def tree_title(self):
		result = self.title
		# try:
		# 	full_path = [self.title]      
		# 	parent = self.parent
		# 	while parent is not None:
		# 		print(parent)
		# 		full_path.append(parent.title)
		# 		parent = parent.parent
		# 	result = ' -> '.join(full_path[::-1]) 
		# except Exception as e:
		# 	print(e)
		# 	result = self.title
		return result

	def __str__(self):     
		result = f'{self.title}'
		result = f'{self.tree_title} ({self.currency})'
		return result

	def save(self, *args, **kwargs):

		if self.currency:
			# try:
			# 	self.items.all().update(currency=self.currency)
			# except:
			# 	pass
			pass

		elif not self.currency:
			alls  = ItemCurrency.objects.all()
			mains = alls.filter(is_main=True)
			if mains.exists():
				self.currency = mains.first()
			elif alls.exists():
				self.currency = alls.first()


		title = self.title.lower().strip()
		# origin_title = title
		# numb = 1
		# while ItemCategory.objects.filter(title=title).exists():
		# 	title = f'{origin_title} ({numb})'
		# 	numb += 1
		self.title = title
		if not self.slug:
			try:
				slug = slugify(translit(self.title, reversed=True), allow_unicode=True) 
			except Exception as e:
				slug = slugify(translit(self.title, 'uk', reversed=True), allow_unicode=True) 
			except Exception as e:
				slug = slugify(translit(self.title, 'ru', reversed=True), allow_unicode=True) 
			except Exception as e:
				slug = slugify(self.title, allow_unicode=True)
			if slug == '':
				slug = slugify(self.title, allow_unicode=True)

			# numb = 1
			# origin_slug = slug 
			# while ItemCategory.objects.filter(slug=slug).exists():
			# 	slug = f'{origin_slug}-{numb}'
			# 	numb += 1



			self.slug  = slug
			cats = ItemCategory.objects.filter(slug=slug)
			# if cats.exists():
			# 	cat = cats.first()
			# print(slug)
			# print(cat)

		super().save(*args, **kwargs)


class ItemImage(BaseMixin):
	item      = SortableForeignKey(verbose_name=_("Товар"), to="item.Item", on_delete=models.SET_NULL, related_name='images', null=True)
	image     = models.ImageField(verbose_name=_('Ссилка зображення'), upload_to=item_image_folder, blank=True, null=True, default='shop/items/test_item.jpg')
	alt       = models.CharField(verbose_name=_("Альт"), max_length=255, blank=True, null=True)

	def __str__(self):
		return "%s" % self.image

	@classmethod
	def modeltranslation_fields(cls):
		fields = [
		    'alt',
		]
		return fields


	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		# img = Image.open(self.image.path)
		# img = img.resize((400, 400), Image.ANTIALIAS)
		# img.save(self.image.path)

	class Meta: 
		verbose_name = _('Зображення товару'); 
		verbose_name_plural = _('Зображення товару'); 
		ordering = ['order',]


class ItemCurrency(BaseMixin):
	name = models.CharField(
		verbose_name=_("Назва"), max_length=255, blank=True, null=True, 
		help_text=_("Наприклад: гривня, долар, рубль, євро")
	)
	symbol = models.CharField(
		verbose_name=_("Символ"), max_length=255, blank=False, null=False, 
		help_text=_("Наприклад: грн., дол., $, руб., Є. Буде відображатись біля ціни в товарі."),
	)
	iso = models.CharField(
		verbose_name=_("Код ІSO"), max_length=255, unique=True, blank=False, null=False, 
		help_text=_("Наприклад: UAH, USD, RUB, EUR")
	)
	rate = models.DecimalField(
		verbose_name=_("Курс"), max_digits=9, decimal_places=7, blank=False, null=True, 
		help_text=_("__")
	)
	is_main = models.BooleanField(
		verbose_name=_("Головна"), default=False,
	)
	class Meta: 
		verbose_name = _('валюта'); 
		verbose_name_plural = _('валюти')
		ordering = ['order',]

	def __str__(self):
		return f"{self.order}:{self.name}"

	@classmethod
	def modeltranslation_fields(cls):
		fields = [
			'symbol',
		]
		return fields

	def save(self, *args, **kwargs):
		# currencies = ItemCurrency.objects.all()
		# old_main_rate = currencies.get(is_main=True).rate
		# currencies.update(is_main=False)
		# if self.is_main:
		# 	self.is_main = True 
		# 	new_main_rate = self.rate
		# 	self.rate = 1
		# for currency in currencies:
		# 	currency.rate = currency.rate / old_main_rate

		# TODO: доделать возможность менять главную валюту. 
		# Пока что в этом нет необходимости, так как для liqpay можно использовать только гривны
		#TODO: периодичная таска, для стягивания валют с банка
		# https://api.privatbank.ua/p24api/exchange_rates?json&date=21.03.2020
		# https://api.privatbank.ua/#p24/exchangeArchive
		# https://api.privatbank.ua/#p24/exchange
		'''
		+  гривня   1   
		-  долар    0.04
		-  евро     0.03
		-  рубль    2.92
		_______
		-  гривня   27   
		+  долар    1    
		-  евро     0.93
		-  рубль    80
		_______
		-  гривня   30   
		-  долар    1.08
		+  евро     1
		-  рубль    86
		_______
		-  гривня   0.34   
		-  долар    0.01  
		-  евро     0.009
		+  рубль    1   

		'''
		super().save(*args, **kwargs)

class ItemMarker(BaseMixin):
	text  = models.CharField(verbose_name=_('Текст'), max_length=255)

	def __str__(self):
		return f"{self.text}"
	
	@classmethod
	def modeltranslation_fields(cls):
		fields = [
			'text',
		]
		return fields


	class Meta:
		verbose_name = _('Маркер')
		verbose_name_plural = _('Маркери')
		ordering = ['order']


class ItemManufacturer(BaseMixin):
	name  = models.CharField(verbose_name=_('Назва'), max_length=255)

	@classmethod
	def modeltranslation_fields(cls):
		fields = [
		    'name',
		]
		return fields

	def __str__(self):
		return f"{self.name}"
	
	class Meta:
		verbose_name = _('Виробник')
		verbose_name_plural = _('Виробники')
		ordering = ['order']


class ItemReview(BaseMixin):
	item    = models.ForeignKey(verbose_name=_("Товар"),  blank=True, null=True, to='item.Item', on_delete=models.SET_NULL, related_name="reviews",)
	user    = models.ForeignKey(verbose_name=_("Автор"),  blank=True, null=True, to=User, on_delete=models.SET_NULL, related_name="reviews",)
	text    = models.CharField(verbose_name=_("Текст"),  blank=True, null=True, max_length=255)
	phone   = models.CharField(verbose_name=_("Телефон"), blank=True, null=True, max_length=255)
	email   = models.CharField(verbose_name=_("E-mail"),  blank=True, null=True, max_length=255)
	name    = models.CharField(verbose_name=_("Ім'я"),    blank=True, null=True, max_length=255)
	rating  = models.CharField(verbose_name=_("Оцінка"),  blank=True, null=True, max_length=255)

	def __str__(self):
		return f"{self.text}{self.rating}"

	class Meta:
		verbose_name = _('Відгук')
		verbose_name_plural = _('Відгуки')
		ordering = ['order']


class ItemCurrencyRatio(models.Model):
	main     = models.ForeignKey(verbose_name=_("Головна валюта"),     to="item.ItemCurrency", on_delete=models.CASCADE, related_name="ratio_main")
	compared = models.ForeignKey(verbose_name=_("Порівнювана валюта"), to="item.ItemCurrency", on_delete=models.CASCADE, related_name="ratio_compared")
	ratio    = models.FloatField(verbose_name=_("Співвідношення"), help_text=(f"Скільки одиниць порівнюваної валюти міститься в 1 одиниці головної валюти"))

	class Meta: 
		verbose_name = _('Співвідношення валют'); 
		verbose_name_plural = _('Співвідношення валют')
		unique_together = ('main','compared')

	def __str__(self):
		return f"{self.main}, {self.compared}"


class ItemStock(BaseMixin):
	text         = models.CharField(verbose_name=_('Наявність'), max_length=255, unique=True)
	availability = models.BooleanField(verbose_name=_('Можливість покупки'), default=True)
	colour       = models.CharField(verbose_name=_('Колір'), choices=STOCK_COLOR_CHOICES, max_length=255, default=1)
	
	def __str__(self):
		return f"{self.text}"
	
	class Meta:
		verbose_name = _('Статус наявності')
		verbose_name_plural = _('Статуси наявності')

	@classmethod
	def modeltranslation_fields(cls):
		fields = [
		    'text',
		]
		return fields





# варіанти

class ItemVariant(BaseMixin):
	item = models.ForeignKey("item.Item", verbose_name=_("Товар"), on_delete=models.CASCADE)



# характеристики

class ItemOption(models.Model):
	item      = models.ForeignKey(verbose_name=_("Товар"), to="item.Item", related_name="options", on_delete=models.SET_NULL, blank=True, null=True)
	name      = models.CharField(verbose_name=_("Назва"), blank=False, null=False, max_length=255)
	price     = models.FloatField(verbose_name=_("Ціна"), blank=False, null=False, default=0)
	help_text = models.TextField(verbose_name=_("Допоміжний текст"), blank=True, null=True)

	@classmethod
	def modeltranslation_fields(cls):
		fields = [
			'name',
			'help_text',
		]
		return fields

	def __str__(self):
		return f'{self.item.title}: {self.name} {self.price}'

	class Meta:
		verbose_name = _('опція товару')
		verbose_name_plural = _('Опції товарів')


class ItemFeatureName(models.Model):
	name = models.CharField(verbose_name=_("Назва характеристики"), max_length=255, unique=True)
	slug = models.SlugField(verbose_name=_("ЧПУ характеристики"), unique=True)
	help_text = models.TextField(verbose_name=_("Допоміжний текст"), blank=True, null=True)

	def __str__(self):
		return f"{self.name}"

	@classmethod
	def modeltranslation_fields(cls):
		fields = [
		    'name',
		]
		return fields

	def save(self, *args, **kwargs):
		if not self.slug:
			try:
				slug = slugify(translit(self.title, reversed=True)) 
			except Exception as e:
				slug = f"{slugify(self.title)}"
			self.slug = slug
		super().save(*args, **kwargs)
	
	class Meta:
		verbose_name = _('назва характеристики')
		verbose_name_plural = _('назви характеристики')


class ItemFeatureValue(models.Model):
	value     = models.TextField(verbose_name=_("Значення"), blank=False, null=False)
	help_text = models.TextField(verbose_name=_("Допоміжний текст"), blank=True, null=True)

	def __str__(self):
		return f"{self.value}"

	@classmethod
	def modeltranslation_fields(cls):
		fields = [
		    'value',
		]
		return fields

	class Meta:
		verbose_name = 'значення характеристики'
		verbose_name_plural = 'значення характеристики'





class ItemFeature(models.Model):
	code     = models.CharField(verbose_name=_("Код"), blank=True, null=True, max_length=255, help_text="Код для прямого звернення до характеристики в шаблоні")
	category = models.ForeignKey(verbose_name=_("Категорія характеристики"), to="item.ItemFeatureCategory", related_name="items", on_delete=models.SET_NULL, blank=True, null=True)
	item     = models.ForeignKey(verbose_name=_("Товар"), to="item.Item", related_name="features", on_delete=models.SET_NULL, blank=True, null=True)
	name     = models.ForeignKey(verbose_name=_("Назва характеристики"), to="item.ItemFeatureName",blank=True, null=True, related_name='features', on_delete=models.SET_NULL)
	# value    = models.TextField(verbose_name=_("Значення характеристики"), blank=False, null=False)
	# value    = models.ForeignKey(verbose_name=_("Значення характеристики"), to="item.ItemFeatureValue", blank=True, null=True, related_name='features', on_delete=models.SET_NULL)
	value    = models.ManyToManyField(verbose_name=_("Значення характеристики"), to="item.ItemFeatureValue", blank=True, related_name='features')

	@classmethod
	def modeltranslation_fields(cls):
		fields = [
		    # 'value',
			# 'name',
		]
		return fields

	def __str__(self):
		return f'{self.name}'

	class Meta:
		verbose_name = _('Характеристика товару')
		verbose_name_plural = _('Характеристики товару')
		unique_together = [
			'name',
			'item'
		]


class ItemFeatureCategory(models.Model):
	name   = models.CharField(verbose_name=_("Назва категорії"), max_length=255, unique=True, blank=True, null=True)

	@classmethod
	def modeltranslation_fields(cls):
		fields = [
		    'name',
		]
		return fields

	def __str__(self):
		return f"{self.name}"

	class Meta:
		verbose_name = _('Категорія характеристики')
		verbose_name_plural = _('Категорії характеристики')

