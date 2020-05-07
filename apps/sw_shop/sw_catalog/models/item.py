from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey

from . import ItemImage, Currency, ItemStock, ItemView
from .. import settings as item_settings

from box.core.models import AbstractPage
from PIL import Image


class Item(AbstractPage):
	if item_settings.MULTIPLE_CATEGORY:
		categories = models.ManyToManyField(
			verbose_name=_("Категорія"), to='sw_catalog.ItemCategory',
			related_name="items", blank=True,
		)
	else:
		category = TreeForeignKey(
			verbose_name=_("Категорія"), to='sw_catalog.ItemCategory',
			related_name="items", on_delete=models.SET_NULL,
			blank=True, null=True,
		)
	markers = models.ManyToManyField(
		verbose_name=_("Маркери"), to='sw_global_config.GlobalMarker',
		related_name='items', blank=True,
	)
	labels = models.ManyToManyField(
		verbose_name=_("Мітки"), to='sw_global_config.GlobalLabel',
		related_name='items', blank=True,
	)
	similars = models.ManyToManyField(
		verbose_name=_("Супутні товари"), to="self",
		related_name="similars_set", blank=True, default=None,
	)
	manufacturer = models.ForeignKey(
		verbose_name=_("Виробник"), to="sw_catalog.ItemManufacturer",
		blank=True, null=True, on_delete=models.SET_NULL,
		related_name='items',
	)
	brand = models.ForeignKey(
		verbose_name=_("Бренд"), to='sw_catalog.ItemBrand',
		related_name='items',
		on_delete=models.SET_NULL, null=True, blank=True,
	)
	in_stock = models.ForeignKey(
		verbose_name=_("Наявність"), to="sw_catalog.ItemStock",
		on_delete=models.SET_NULL, blank=True, null=True,
		help_text=' ',
	)
	unit = models.ForeignKey(
		verbose_name=_("Одиниці вимірювання"), blank=True, null=True,
		to='sw_catalog.ItemUnit', on_delete=models.SET_NULL,
	)
	amount = models.PositiveIntegerField(
		verbose_name=_("Кількість"), blank=True, null=True, default=None,
		help_text=_('0 - товар відсутній. Порожнє поле - необмежена кількість.'),
	)

	currency = models.ForeignKey(
		verbose_name=_("Валюта"),    to="sw_currency.Currency",
		related_name="items", on_delete=models.SET_NULL, 
		blank=True, null=True,
	)
	DISCOUNT_TYPE_CHOICES = (
		("p", "%"),
		("v", "сумма"),
	)
	discount_type = models.CharField(
		verbose_name=_("Тип знижки"), default="v", max_length=255,
		choices=DISCOUNT_TYPE_CHOICES,
	)
	discount = models.FloatField(
		verbose_name=_("знижка"), default=0, max_length=255,
		# validators=[MinValueValidator(0), MaxValueValidator(100)],
	)
	# TODO: rest_framework.serializers.ModelSerializer чогось не серіалізує DecimalField
	# price        = models.DecimalField(
	# verbose_name=_("Нова ціна"),  max_digits=10, decimal_places=2, default=0)
	price = models.FloatField(
		verbose_name=_("Актуальна ціна"), blank=True, null=True,
	)

	def get_final_price(self):
		final_price = self.converted_discount_price() or self.converted_price()
		return final_price
	
	def converted_price(self):
		price = 0 
		if self.price and self.currency:
			price = self.price * self.currency.get_rate()
		return price

	def converted_discount_price(self):
		price = 0 
		if self.discount_price and self.currency:
			price = self.price * self.currency.get_rate()
		return price

	def discount_price(self):
		price = 0
		if self.price and self.discount:
			discount = self.discount
			if self.discount_type == 'p':
				discount = self.price * (discount / 100)
			price = self.price - discount
		return round(price)
	
	def main_currency(self):
		return Currency.objects.get(is_main=True)

	def clean(self):
		from django.core.validators import ValidationError 
		if self.discount_type == 'v' and not (self.price > self.discount):
			raise ValidationError('Знижка мусить бути мешною за ціну')
		if self.discount_type == 'p' and not (self.discount < 100):
			raise ValidationError('Знижка мусить бути мешною за 100%')

	def views(self):
		return ItemView.objects.filter(item=self).count()

	def add_view(self, request):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		if request.session.session_key:
			view, _ = ItemView.objects.get_or_create(sk=request.session.session_key, item=self)
			view.ip = ip 
			view.save()

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
			self.image.save(
				image.name.split("/")[-1], 
				ContentFile(image.read()),
			)

	def get_absolute_url(self):
		return reverse(item_settings.ITEM_URL_NAME, kwargs={"slug": self.slug})

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		self.resize_image(self.image)

	def __str__(self):
		return f"{self.title}, {self.slug}"
	
	class Meta: 
		verbose_name = _('товар'); 
		verbose_name_plural = _('товари')
		ordering = ['order']
