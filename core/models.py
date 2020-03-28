from django.db import models 
from django.utils.translation import gettext_lazy as _
from django.utils import timezone 
from django.conf import settings

from tinymce import HTMLField
from adminsortable.models import SortableMixin

from .managers import *

from box.core.helpers import get_admin_url

__all__ = [
    "BaseMixin",
    "AbstractPage",
]


class BaseMixin(models.Model):
	# code == int, тому що для товара потрібно інкрементування.
	code            = models.IntegerField(verbose_name=_("Код"),  blank=True, null=True, unique=True)
	order           = models.PositiveIntegerField(verbose_name=_("Порядок"), default=0, blank=False, null=False)
	is_active       = models.BooleanField(verbose_name=_("Активність"), default=True, help_text=_("Відображення на сайті"))
	created         = models.DateTimeField(verbose_name=_("Створено"), default=timezone.now)
	updated         = models.DateTimeField(verbose_name=_("Оновлено"), auto_now_add=False, auto_now=True, blank=True, null=True)
	
	objects         = BasicManager()
	active_objects  = ActiveManager()

	# TODO: розібратись з is_active, related_name, фільтруванням
	class Meta:
		abstract = True 

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

	def get_admin_url(self):
		return get_admin_url(self)
	



class AbstractPage(BaseMixin):
	# code == slug, тому що для контенту потрібен виклик в шаблоні по "змінній"
	# UPD: товар наслідується від цього класу, тому має бути інтежер
	# code       = models.SlugField(verbose_name=_("Код"), max_length=255, blank=False, null=False, unique=True)
	meta_title = models.TextField(verbose_name=_("Мета-заголовок"),     blank=True, null=True, help_text=_("Заголовок сторінки в браузері, який відображається у видачі пошукових систем"))
	meta_descr = models.TextField(verbose_name=_("Мета-опис"),          blank=True, null=True, help_text=_("__"))
	meta_key   = models.TextField(verbose_name=_("Ключові слова"),      blank=True, null=True, help_text=_("Список ключових слів"))
	slug       = models.SlugField(verbose_name=_("Посилання"),          max_length=255, null=True, blank=False, unique=True)
	alt        = models.CharField(verbose_name=_("Альт до картинки"),   blank=True, null=True, max_length=255)
	image      = models.ImageField(verbose_name=_("Картинка"), blank=True, null=True, upload_to='shop/category')
	title      = models.CharField(verbose_name=_("Назва"),              blank=False, null=False, max_length=255, )
	description= HTMLField(verbose_name=_("Опис"), blank=True, null=True)

	class Meta:
		abstract = True
	
	def save(self, *args, **kwargs):
		if not self.meta_title and self.title:
			self.meta_title = self.title 
		if not self.meta_descr and self.description:
			self.meta_descr = self.description
		super().save(*args, **kwargs)
	
	def __str__(self):
		return f'{self.title}'
	
	@property
	def image_url(self):
		if self.image:
			url = self.image.url
		else:
			url = settings.NO_ITEM_IMAGE
		return url 

	@property
	def image_path(self):
		image = ''
		if self.image:
			image = self.image.path
		return image

	@classmethod
	def modeltranslation_fields(cls):
		fields = [
			'meta_title',
			'meta_descr',
			'meta_key',
			'title',
			'description',
			'alt',
		]
		return fields 
	
	def get_absolute_url(self):
		return reverse("page", kwargs={"code": self.code})
	

