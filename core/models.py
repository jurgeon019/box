from django.db import models 
from django.utils.translation import gettext_lazy as _
from django.utils import timezone 
from box.core import settings as core_settings 

from tinymce import HTMLField
from adminsortable.models import SortableMixin

from .managers import *

from box.core.helpers import get_admin_url

__all__ = [
    "BaseMixin",
    "AbstractPage",
]


class BaseMixin(models.Model):
	"""
	У BaseMixin code blank=True, null=True тому що від нього наслідуються об'єкти,
	у яких коду є опціональним(Item, Post, ItemCategory, PostCategory, AbstractContent і тд.) 
	"""
	code            = models.SlugField(
		verbose_name=_("Код"), 
		blank=True, null=True,
		unique=True, 
		# default=None, 
		# unique=False, 
		max_length=255, help_text=("Допоміжний код для виводу в шаблоні")
	)
	# def save(self, *args, **kwargs):
	# 	if self.code:
	# 		i = 0
	# 		code = self.code
	# 		while self._meta.model.objects.all().filter(code=code).exists():
	# 			code = f'{code}_{i}'
	# 			print(code)
	# 			i+=1
	# 		self.code = code 
	# 	super().save(*args, **kwargs)
			
	order           = models.PositiveIntegerField(
		verbose_name=_("Порядок"), default=0, blank=False, null=False
	)
	is_active       = models.BooleanField(
		verbose_name=_("Активність"), default=True, help_text=_("Відображення на сайті")
	)
	created         = models.DateTimeField(
		verbose_name=_("Створено"), default=timezone.now
	)
	updated         = models.DateTimeField(
		verbose_name=_("Оновлено"), auto_now_add=False, auto_now=True, blank=True, null=True
	)
	
	objects         = BasicManager()
	active_objects  = ActiveManager()

	# TODO: розібратись з is_active, related_name, фільтруванням
	class Meta:
		abstract = True 

	def get_admin_url(self):
		return get_admin_url(self)
	
	@classmethod
	def modeltranslation_fields(self):
		return []


class AbstractPage(BaseMixin):
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
		from box.core.signals import handle_slug 
		if not self.meta_title and self.title:
			self.meta_title = self.title 
		if not self.alt and self.title:
			self.alt = self.title 
		if not self.meta_descr and self.description:
			self.meta_descr = self.description
		handle_slug(self)
		print(self.title, self.code)
		super().save(*args, **kwargs)

	def __str__(self):
		return f'{self.title}'
	
	@property
	def image_url(self):
		if self.image:
			url = self.image.url
		else:
			url = core_settings.IMAGE_NOT_FOUND
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
		return reverse("page", kwargs={"slug": self.slug})
	

