from ._imports import * 
from django.utils.translation import gettext_lazy as _


class ItemCurrency(models.Model):
	name = models.CharField(
		verbose_name=_("Назва"), max_length=255, blank=True, null=True, 
		help_text=_("Наприклад: гривня, долар, рубль, євро")
	)
	symbol = models.CharField(
		verbose_name=_("Символ"), max_length=255, blank=False, null=False, 
		help_text=_("Наприклад: грн., дол., $, руб., Є. Буде відображатись біля ціни в товарі."),
	)
	code = models.SlugField(
		verbose_name=_("Код ІSO"), max_length=255, unique=True, blank=False, null=False, 
		help_text=_("Наприклад: UAH, USD, RUB, EUR")
	)
	rate = models.DecimalField(
		verbose_name=_("Курс"), max_digits=9, decimal_places=7, blank=False, null=True, 
		help_text=_("__")
	)
	is_main = models.BooleanField(
		verbose_name=_("Головна"), default=False,
	)
	class Meta: 
		verbose_name = _('валюта'); 
		verbose_name_plural = _('валюти')

	def __str__(self):
		return f"{self.code}"

	@classmethod
	def modeltranslation_fields(cls):
		fields = [
			'symbol',
		]
		return fields

	def get_admin_url(self):
		return get_admin_url(self)


	def save(self, *args, **kwargs):
		if self.code:
			if not self.symbol:
				self.symbol = self.code 
			if not self.name:
				self.name = self.code
		# currencies = ItemCurrency.objects.all()
		# old_main_rate = currencies.get(is_main=True).rate
		# currencies.update(is_main=False)
		# if self.is_main:
		# 	self.is_main = True 
		# 	new_main_rate = self.rate
		# 	self.rate = 1
		# for currency in currencies:
		# 	currency.rate = currency.rate / old_main_rate

		# TODO: доделать возможность менять главную валюту. 
		# Пока что в этом нет необходимости, так как для liqpay можно использовать только гривны
		#TODO: периодичная таска, для стягивания валют с банка
		# https://api.privatbank.ua/p24api/exchange_rates?json&date=21.03.2020
		# https://api.privatbank.ua/#p24/exchangeArchive
		# https://api.privatbank.ua/#p24/exchange
		'''
		+  гривня   1   
		-  долар    0.04
		-  евро     0.03
		-  рубль    2.92
		_______
		-  гривня   27   
		+  долар    1    
		-  евро     0.93
		-  рубль    80
		_______
		-  гривня   30   
		-  долар    1.08
		+  евро     1
		-  рубль    86
		_______
		-  гривня   0.34   
		-  долар    0.01  
		-  евро     0.009
		+  рубль    1   

		'''
		super().save(*args, **kwargs)





class ItemCurrencyRatio(models.Model):
	main     = models.ForeignKey(verbose_name=_("Головна валюта"),     to="sw_item.ItemCurrency", on_delete=models.CASCADE, related_name="ratio_main")
	compared = models.ForeignKey(verbose_name=_("Порівнювана валюта"), to="sw_item.ItemCurrency", on_delete=models.CASCADE, related_name="ratio_compared")
	ratio    = models.FloatField(verbose_name=_("Співвідношення"), help_text=(f"Скільки одиниць порівнюваної валюти міститься в 1 одиниці головної валюти"))

	class Meta: 
		verbose_name = _('Співвідношення валют'); 
		verbose_name_plural = _('Співвідношення валют')
		unique_together = ('main','compared')

	def __str__(self):
		return f"{self.main}, {self.compared}"

