from django.utils.translation import gettext_lazy as _
from django.db import models 
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse 

from mptt.models import MPTTModel, TreeForeignKey

from . import ItemImage, ItemCurrency, ItemStock
from .. import settings as item_settings

from box.core.models import AbstractPage


class Item(AbstractPage):
	if item_settings.MULTIPLE_CATEGORY:
		categories   = models.ManyToManyField(
			verbose_name=_("Категорія"), to='sw_catalog.ItemCategory', related_name="items", blank=True)    
	else:
		category     = TreeForeignKey(
			verbose_name=_("Категорія"), to='sw_catalog.ItemCategory', related_name="items", on_delete=models.SET_NULL, blank=True, null=True)    
	markers      = models.ManyToManyField(
		verbose_name=_("Маркери"), to='sw_catalog.ItemMarker', related_name='items', blank=True)
	similars     = models.ManyToManyField(
		verbose_name=_("Супутні товари"), to="self", related_name="similars_set", blank=True, default=None)
	manufacturer = models.ForeignKey(
		verbose_name=_("Виробник"), to="sw_catalog.ItemManufacturer", blank=True, null=True, on_delete=models.SET_NULL, related_name='items')
	brand        = models.ForeignKey(
		verbose_name=_("Бренд"), to='sw_catalog.ItemBrand', related_name='items', on_delete=models.SET_NULL, null=True, blank=True)
	in_stock     = models.ForeignKey(
		verbose_name=_("Наявність"), to="sw_catalog.ItemStock", on_delete=models.SET_NULL, blank=True, null=True, 
		help_text=' ',
	)
	currency     = models.ForeignKey(
		verbose_name=_("Валюта"),    to="sw_catalog.ItemCurrency",     related_name="items", on_delete=models.SET_NULL, help_text=("Якщо залишити порожнім, то буде встановлена валюта категорії, у якій знаходиться товар"), blank=True, null=True)
	# old_price    = models.DecimalField(
	# verbose_name=_("Стара ціна"), max_digits=10, decimal_places=2, default=0)
	# price        = models.DecimalField(
	# verbose_name=_("Нова ціна"),  max_digits=10, decimal_places=2, default=0)
	# TODO: rest_framework.serializers.ModelSerializer чогось не серіалізує DecimalField
	old_price    = models.FloatField(
		verbose_name=_("Стара ціна"), blank=True, null=True)
	new_price    = models.FloatField(
		verbose_name=_("Актуальна ціна"), blank=True, null=True)
	discount     = models.FloatField(
		verbose_name=_("Скидка"), blank=True, null=True, default=0,
		validators=[MinValueValidator(0), MaxValueValidator(100)],
	)
	unit  = models.ForeignKey(
		verbose_name=_("Одиниці вимірювання"), blank=True, null=True,
		to='sw_catalog.ItemUnit', on_delete=models.SET_NULL,
	)
	amount       = models.PositiveIntegerField(
		verbose_name=_("Кількість"), blank=True, null=True, default=None, 
		help_text=_('0 - товар відсутній. Порожнє поле - необмежена кількість.'),
	)

	class Meta: 
		verbose_name = _('товар'); 
		verbose_name_plural = _('товари')
		ordering = ['order']

	def __str__(self):
		return f"{self.title}, {self.slug}"

	# @classmethod
	# def modeltranslation_fields(self):
	# 	return super().modeltranslation_fields() + ['units',]

	def save(self, *args, **kwargs):
		# self.handle_currency(*args, **kwargs)
		# self.handle_category(*args, **kwargs) #TODO:
		self.handle_availability(*args, **kwargs)
		super().save(*args, **kwargs)
		self.resize_image(self.image)

	def handle_availability(self, *args, **kwargs):
		available_stocks   = ItemStock.objects.filter(availability=True)
		unavailable_stocks = ItemStock.objects.filter(availability=False)

		if self.amount == 0:
			if unavailable_stocks.exists():
				self.in_stock = unavailable_stocks.first()
	
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
		from django.urls.exceptions import NoReverseMatch
		try:
			return reverse(item_settings.ITEM_URL_NAME, kwargs={"slug": self.slug})
		except NoReverseMatch as e:
			print('e:', e)
			return 

	@property
	def is_in_stock(self):
		return bool(self.amount)
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
		if item_settings.MULTIPLE_CATEGORY:
			for category in categories:
				self.categories.add(category)
		else:
			self.category = categories[-1]
		self.save()

	def in_cart(self, request):
		from box.apps.sw_shop.sw_cart.models import CartItem
		from box.apps.sw_shop.sw_cart.utils import get_cart
		in_cart = self.id in CartItem.objects.filter(cart=get_cart(request)).values_list('item__id', flat=True)
		return in_cart 

