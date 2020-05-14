from django.utils.translation import gettext_lazy as _
from django.db import models 
from box.core.sw_solo.models import SingletonModel 


class ParseCurrency(models.Model):
	parse_choices = (
		("UAH","UAH"),
		("RUB","RUB"),
		("EUR","EUR"),
		("USD","USD"),
		("AZN","AZN"),
		("BYN","BYN"),
		("CAD","CAD"),
		("CHF","CHF"),
		("CZK","CZK"),
		("UZS","UZS"),
	)
	config = models.ForeignKey(
		to="sw_currency.CurrencyConfig", on_delete=models.CASCADE,
	)
	name = models.CharField(
		verbose_name=_("Назва"), choices=parse_choices, max_length=255,
		blank=True, unique=True 
	)
	
	def save(self, *args, **kwargs):
		if not self.config:
			self.config = CurrencyConfig.get_solo()
		super().save(*args, **kwargs)
		
	def __str__(self):
		return f'{self.name}'

	class Meta:
		verbose_name = _("Валюта для парсингу")
		verbose_name_plural = _("Валюти для парсингу")
		unique_together = [
			'name','config'
		]


class CurrencyConfig(SingletonModel):
	field_choices = (
		("purchase","по курсу купівлі"),
		("sale","по курсу продажі"),
	)
	main_field = models.CharField(
		verbose_name=_("Поле для конвертації"), default="purchase",
		choices=field_choices, max_length=255,
	)
	# TODO: з адмінки вибирати джерело парсингу валют(pb, нацбанк і тд)
	def get_currencies(self):
		return ParseCurrency.objects.filter(config=self)

	class Meta:
		verbose_name = _("Налаштування валют")
		verbose_name_plural = verbose_name


class Currency(models.Model):
	# name = models.CharField(
	# 	verbose_name=_("Назва"), max_length=255, blank=True, null=True, 
	# 	help_text=_("Наприклад: гривня, долар, рубль, євро")
	# )
	symbol = models.CharField(
		verbose_name=_("Символ"), max_length=255, 
		help_text=_("Наприклад: грн., дол., $, руб., Є. Буде відображатись біля ціни в товарі."),
	)
	code = models.SlugField(
		verbose_name=_("Код ІSO"), max_length=255, unique=True, 
	)
	sale_rate = models.FloatField(
		verbose_name=_("Курс продажі"), 
		blank=False, null=True, 
	)
	purchase_rate = models.FloatField(
		verbose_name=_("Курс купівлі"), 
		blank=False, null=True, 
	)
	is_main = models.BooleanField(
		verbose_name=_("Головна"), default=False,
	)

	def get_rate(self): 
		main_field = CurrencyConfig.get_solo().main_field
		if main_field == "sale":
			return self.sale_rate 
		elif main_field == "purchase":
			return self.purchase_rate

	class Meta: 
		verbose_name = _('валюта'); 
		verbose_name_plural = _('валюти')
	
	def save(self, *args, **kwargs):
		if not self.symbol:
			self.symbol = self.code 
		objs = self._meta.model.objects.exclude(id=self.id)
		if self.is_main and objs.exists():
			objs.update(is_main=False)
			self.is_main = True 
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.code}"

	@classmethod
	def modeltranslation_fields(cls):
		return [
			'symbol',
		]

	def get_admin_url(self):
		return get_admin_url(self)
	


