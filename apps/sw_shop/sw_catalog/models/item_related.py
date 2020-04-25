from django.utils.translation import gettext_lazy as _
# from ._imports import * 
from django.db import models 
from box.core.models import AbstractPage, BaseMixin
from adminsortable.admin import SortableAdmin, NonSortableParentAdmin, SortableStackedInline
from adminsortable.fields import SortableForeignKey
from ..utils import generate_unique_slug, item_image_folder
from django.contrib.auth import get_user_model
from django.conf import settings 
from box.core import settings as core_settings


User = get_user_model()


class ItemLabel(models.Model):
	text  = models.CharField(verbose_name=_('Текст'), max_length=255)
	
	@classmethod
	def modeltranslation_fields(cls): return ['text']

	def __str__(self): return f"{self.text}"

	class Meta:
		verbose_name = _('мітка товарів')
		verbose_name_plural = _('мітки товарів')


class ItemMarker(models.Model):
	name  = models.CharField(verbose_name=_('Назва'), max_length=255)
	code  = models.SlugField(
		verbose_name=_("Код"), unique=True
	)
	def __str__(self): return f"{self.name}"

	@classmethod
	def modeltranslation_fields(cls): return ['name']

	class Meta:
		verbose_name = _('маркер товарів')
		verbose_name_plural = _('маркери товарів')


class ItemUnit(models.Model):
	name = models.CharField(
		verbose_name=_("Назва"), unique=True, max_length=255,
	)

	def __str__(self):
		return f'{self.name}'
	
	@classmethod
	def modeltranslation_fields(self):
		return [
			'name',
		]
	
	class Meta:
		verbose_name = _("одиниця вимірювання")
		verbose_name_plural = _("одиниці вимірювання")



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


class ItemImage(BaseMixin):
	item      = SortableForeignKey(
		verbose_name=_("Товар"), to="sw_catalog.Item", 
		on_delete=models.SET_NULL, 
		related_name='images', null=True,
	)
	image     = models.ImageField(
		verbose_name=_('Ссилка зображення'), upload_to=item_image_folder, 
		blank=True, null=True,
	)
	alt       = models.CharField(
		verbose_name=_("Альт"), max_length=255, blank=True, null=True,
	)

	def __str__(self):
		return "%s" % self.image

	@classmethod
	def modeltranslation_fields(cls):
		fields = [
		    'alt',
		]
		return fields
	
	def image_url(self):
		image_url = core_settings.IMAGE_NOT_FOUND
		if self.image: image_url = self.image.url 
		return image_url


	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		# img = Image.open(self.image.path)
		# img = img.resize((400, 400), Image.ANTIALIAS)
		# img.save(self.image.path)

	class Meta: 
		verbose_name = _('Зображення товару'); 
		verbose_name_plural = _('Зображення товару'); 
		ordering = ['order',]



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
	item    = models.ForeignKey(verbose_name=_("Товар"),  blank=True, null=True, to="sw_catalog.Item", on_delete=models.SET_NULL, related_name="reviews",)
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


class ItemStock(BaseMixin):
	STOCK_COLOR_CHOICES = (
		('g', "green"),
		('o', "orange"),
		('r', "red"),
	)
	text         = models.CharField(verbose_name=_('Текст'), max_length=255, unique=True)
	availability = models.BooleanField(verbose_name=_('Можливість покупки'), default=True)
	# availability = models.NullBooleanField(verbose_name=_('Можливість покупки'), default=True, null=True)
	colour       = models.CharField(verbose_name=_('Колір'), choices=STOCK_COLOR_CHOICES, max_length=255, default=1)

	def __str__(self):
		return f"{self.text}"
	
	class Meta:
		verbose_name = _('статус наявності')
		verbose_name_plural = _('статуси наявності')

	@classmethod
	def modeltranslation_fields(cls):
		fields = [
		    'text',
		]
		return fields




