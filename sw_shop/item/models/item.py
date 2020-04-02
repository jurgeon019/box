from django.utils.translation import gettext_lazy as _

from ._imports import * 
from . import ItemImage, ItemCurrency, ItemStock, ItemCurrencyRatio

from .. import settings as item_settings



class Item(AbstractPage):
	if item_settings.MULTIPLE_CATEGORY:
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
	units        = models.CharField(verbose_name=_("Одиниці вимірювання"), blank=True, null=True, max_length=255)
	amount       = models.PositiveIntegerField(verbose_name=_("Кількість"), blank=True, null=True, default=None, help_text='"Кількість" в пріорітеті над "наявністю"')
	# rating       = models.FloatField(verbose_name=_("Рейтинг"),)

	class Meta: 
		verbose_name = _('товар'); 
		verbose_name_plural = _('товари')
		ordering = ['order']

	def __str__(self):
		return f"{self.title}, {self.slug}"

	def save(self, *args, **kwargs):
		# self.handle_currency(*args, **kwargs)
		# self.handle_category(*args, **kwargs) #TODO:
		self.handle_availability(*args, **kwargs)
		super().save(*args, **kwargs)
		self.resize_image(self.image)

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
			if item_settings.MULTIPLE_CATEGORY:
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
		if item_settings.MULTIPLE_CATEGORY:
			for category in categories:
				self.categories.add(category)
		else:
			self.category = categories[-1]
		self.save()

	def get_categories(self, ):

		return categories 
	
	def in_cart(self, request):
		from box.sw_shop.cart.models import CartItem
		from box.sw_shop.cart.utils import get_cart
		in_cart = self.id in CartItem.objects.filter(cart=get_cart(request)).values_list('item__id', flat=True)
		return in_cart 

