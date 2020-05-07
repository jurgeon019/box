from django.utils.translation import gettext_lazy as _
from django.db import models 


class Currency(models.Model):
	# name = models.CharField(
	# 	verbose_name=_("Назва"), max_length=255, blank=True, null=True, 
	# 	help_text=_("Наприклад: гривня, долар, рубль, євро")
	# )
	# symbol = models.CharField(
	# 	verbose_name=_("Символ"), max_length=255, blank=False, null=False, 
	# 	help_text=_("Наприклад: грн., дол., $, руб., Є. Буде відображатись біля ціни в товарі."),
	# )
	code = models.SlugField(
		verbose_name=_("Код ІSO"), max_length=255, unique=True, blank=False, null=False, 
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
		# TODO: CurrencyConfig.get_solo().main_field
		return self.sale_rate or self.purchase_rate

	class Meta: 
		verbose_name = _('валюта'); 
		verbose_name_plural = _('валюти')

	def __str__(self):
		return f"{self.code}"

	@classmethod
	def modeltranslation_fields(cls):
		fields = [
		]
		return fields

	def get_admin_url(self):
		return get_admin_url(self)
	
