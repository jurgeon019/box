from adminsortable.models import SortableMixin
from django.db import models 
from django.utils.translation import gettext_lazy as _
from django.utils import timezone 
from .managers import *
from tinymce import HTMLField
from django.conf import settings
	

__all__ = [
    "BaseMixin",
    "Page",
]


class BaseMixin(models.Model):
	order      = models.PositiveIntegerField(verbose_name=_("Порядок"), default=0, blank=False, null=False)
	is_active  = models.BooleanField(("Активність"), default=True, help_text=_("Відображення на сайті"))
	created    = models.DateTimeField(verbose_name=_("Створено"), default=timezone.now)
	updated    = models.DateTimeField(verbose_name=_("Оновлено"), auto_now_add=False, auto_now=True, blank=True, null=True)
	objects    = BasicManager()
	default_objects = models.Manager()

	class Meta:
		abstract = True 


class Page(BaseMixin):
	meta_title = models.TextField(verbose_name=_("Мета-заголовок"),     blank=True, null=True, help_text=_("Заголовок сторінки в браузері, який відображається у видачі пошукових систем"))
	meta_descr = models.TextField(verbose_name=_("Мета-опис"),          blank=True, null=True, help_text=_("__"))
	meta_key   = models.TextField(verbose_name=_("Ключові слова"),      blank=True, null=True, help_text=_("Список ключових слів"))
	slug       = models.SlugField(verbose_name=_("Посилання"),          max_length=255, null=True, blank=False, unique=True)
	code       = models.SlugField(verbose_name=_("Код"),                max_length=255, null=False, blank=True, unique=True, default=1)
	alt        = models.CharField(verbose_name=_("Альт до картинки"),   blank=True, null=True, max_length=255)
	image      = models.ImageField(verbose_name=_("Картинка"), blank=True, null=True, upload_to='shop/category')
	title      = models.CharField(verbose_name=_("Назва"),              blank=False, null=False, max_length=255, )
	description= HTMLField(verbose_name=_("Опис"), blank=True, null=True)

	class Meta:
		abstract = True
	
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
