from django.utils.translation import gettext_lazy as _ 
from django.db import models 
from django.conf import settings 
from box.core.sw_solo.models import SingletonModel
from box.apps.sw_payment.liqpay import settings as liqpay_settings



class LiqpayConfig(SingletonModel):
  liqpay_public_key   = models.TextField(
    _("Публічний ключ"), blank=False,  null=False, 
    default=liqpay_settings.LIQPAY_PUBLIC_KEY,
  )
  liqpay_private_key  = models.TextField(
    _("Приватний ключ"), blank=False,  null=False, 
    default=liqpay_settings.LIQPAY_PRIVATE_KEY,
  )
  liqpay_sandbox_public_key   = models.TextField(
    _("Тестовий публічний ключ"), blank=False,  null=False, 
    default=liqpay_settings.LIQPAY_SANDBOX_PUBLIC_KEY,
  )
  liqpay_sandbox_private_key  = models.TextField(
    _("Тестовий приватний ключ"), blank=False,  null=False, 
    default=liqpay_settings.LIQPAY_SANDBOX_PRIVATE_KEY,
  )
  sandbox_mode = models.BooleanField(
    verbose_name=_("Тестовий режим"), default=1
  )
  
  @classmethod
  def modeltranslation_fields(cls):
      return []
  
  class Meta:
    verbose_name        = _('налаштування Liqpay')
    verbose_name_plural = verbose_name


class LiqpayTransaction(models.Model):
  # timestamp           = models.DateTimeField(verbose_name='Час',auto_now_add=True, blank=True, null=True)
  timestamp           = models.CharField(verbose_name='Час', max_length=255, blank=True, null=True)
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
  order               = models.CharField(verbose_name='Заказ', max_length=255, blank=True, null=True)
       
  def __str__(self):
    return f'{self.order}|{self.amount}|{self.currency}'

  class Meta: 
    verbose_name = _('трансакція liqpay')
    verbose_name_plural = _('трансакції liqpay') 


#     action              = response.get('action', '')
#     payment_id          = response.get('payment_id', '')
#     status              = response.get('status', '')
#     version             = response.get('version', '')
#     type                = response.get('type', '')
#     paytype             = response.get('paytype', '')
#     public_key          = response.get('public_key', '')
#     acq_id              = response.get('acq_id', '')
#     order_id            = response.get('order_id', '')
#     liqpay_order_id     = response.get('liqpay_order_id', '')
#     description         = response.get('description', '')
#     sender_phone        = response.get('sender_phone', '')
#     sender_first_name   = response.get('sender_first_name', '')
#     sender_last_name    = response.get('sender_last_name', '')
#     sender_card_mask2   = response.get('sender_card_mask2', '')
#     sender_card_bank    = response.get('sender_card_bank', '')
#     sender_card_type    = response.get('sender_card_type', '')
#     sender_card_country = response.get('sender_card_country', '')
#     ip                  = response.get('ip', '')
#     amount              = response.get('amount', '')
#     currency            = response.get('currency', '')
#     sender_commission   = response.get('sender_commission', '')
#     receiver_commission = response.get('receiver_commission', '')
#     agent_commission    = response.get('agent_commission', '')
#     amount_debit        = response.get('amount_debit', '')
#     amount_credit       = response.get('amount_credit', '')
#     commission_debit    = response.get('commission_debit', '')
#     commission_credit   = response.get('commission_credit', '')
#     currency_debit      = response.get('currency_debit', '')
#     currency_credit     = response.get('currency_credit', '')
#     sender_bonus        = response.get('sender_bonus', '')
#     amount_bonus        = response.get('amount_bonus', '')
#     mpi_eci             = response.get('mpi_eci', '')
#     is_3ds              = response.get('is_3ds', '')
#     language            = response.get('language', '')
#     create_date         = response.get('create_date', '')
#     end_date            = response.get('end_date', '')
#     transaction_id      = response.get('transaction_id', '')
