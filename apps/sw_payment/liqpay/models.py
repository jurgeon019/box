from django.db import models 

from django.conf import settings 
from box.core.sw_solo.models import SingletonModel



from django.utils.translation import gettext_lazy as _ 



class Payment(models.Model):
  if 'box.apps.sw_shop.sw_order' in settings.INSTALLED_APPS:
    order               = models.OneToOneField(verbose_name='Замовлення',to='sw_order.Order', on_delete=models.CASCADE, blank=True, null=True)
  timestamp           = models.DateTimeField(verbose_name='Час',auto_now_add=True, blank=True, null=True)
  status              = models.CharField(verbose_name='Статус', max_length=255, blank=True, null=True)
  ip                  = models.CharField(verbose_name='ІР', max_length=255, blank=True, null=True)
  amount              = models.CharField(verbose_name='Сумма', max_length=255, blank=True, null=True)
  currency            = models.CharField(verbose_name='Валюта', max_length=255, blank=True, null=True)
  sender_phone        = models.CharField(verbose_name='Номер телефону', max_length=255, blank=True, null=True)
  sender_first_name   = models.CharField(verbose_name='Імя', max_length=255, blank=True, null=True)
  sender_last_name    = models.CharField(verbose_name='Прізвище', max_length=255, blank=True, null=True)
  sender_card_mask2   = models.CharField(verbose_name='Номер карти', max_length=255, blank=True, null=True)
  sender_card_bank    = models.CharField(verbose_name='Банк', max_length=255, blank=True, null=True)
  sender_card_type    = models.CharField(verbose_name='Тип карти', max_length=255, blank=True, null=True)
  sender_card_country = models.CharField(verbose_name='Країна', max_length=255, blank=True, null=True)

  def __str__(self):
    return f'{self.order}|{self.amount}|{self.currency}'

  class Meta: 
    verbose_name = 'Оплата'
    verbose_name_plural = 'Оплати' 




class LiqpayConfig(SingletonModel):
  from box.apps.sw_payment.liqpay import settings as liqpay_settings
  liqpay_public_key   = models.TextField(
    _("Публічний ключ лікпею"), blank=False, 
    null=False, default=liqpay_settings.LIQPAY_PUBLIC_KEY,
  )
  liqpay_private_key  = models.TextField(
    _("Приватний ключ лікпею"), blank=False, 
    null=False, default=liqpay_settings.LIQPAY_PRIVATE_KEY,
  )
  
  @classmethod
  def modeltranslation_fields(cls):
      fields = [
      ]
      return fields
  
  class Meta:
    verbose_name        = _('Налаштування оплати')
    verbose_name_plural = _('Налаштування оплати')
