from ._imports import * 
from django.utils.translation import gettext_lazy as _


# # варіанти

class ItemVariant(BaseMixin):
	item = models.ForeignKey("sw_item.Item", verbose_name=_("Товар"), on_delete=models.CASCADE)



# характеристики

class ItemOption(models.Model):
	item      = models.ForeignKey(verbose_name=_("Товар"), to="sw_item.Item", related_name="options", on_delete=models.SET_NULL, blank=True, null=True)
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
	category = models.ForeignKey(verbose_name=_("Категорія характеристики"), to="sw_item.ItemFeatureCategory", related_name="items", on_delete=models.SET_NULL, blank=True, null=True)
	item     = models.ForeignKey(verbose_name=_("Товар"), to="sw_item.Item", related_name="features", on_delete=models.SET_NULL, blank=True, null=True)
	name     = models.ForeignKey(verbose_name=_("Назва характеристики"), to="sw_item.ItemFeatureName",blank=True, null=True, related_name='features', on_delete=models.SET_NULL)
	# value    = models.TextField(verbose_name=_("Значення характеристики"), blank=False, null=False)
	# value    = models.ForeignKey(verbose_name=_("Значення характеристики"), to="sw_item.ItemFeatureValue", blank=True, null=True, related_name='features', on_delete=models.SET_NULL)
	value    = models.ManyToManyField(verbose_name=_("Значення характеристики"), to="sw_item.ItemFeatureValue", blank=True, related_name='features')

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

