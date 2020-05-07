from django.utils.translation import gettext_lazy as _ 
from django.db import models 
from django.conf import settings 
from box.core.sw_solo.models import SingletonModel
from box.apps.sw_payment.liqpay import settings as liqpay_settings
from django.conf import settings 


class LiqpayConfig(SingletonModel):
  liqpay_public_key   = models.TextField(
    _("Публічний ключ"), blank=False,  null=False, 
    default=settings.LIQPAY_PUBLIC_KEY,
  )
  liqpay_private_key  = models.TextField(
    _("Приватний ключ"), blank=False,  null=False, 
    default=settings.LIQPAY_PRIVATE_KEY,
  )
  liqpay_sandbox_public_key   = models.TextField(
    _("Тестовий публічний ключ"), blank=False,  null=False, 
    default=settings.LIQPAY_SANDBOX_PUBLIC_KEY,
  )
  liqpay_sandbox_private_key  = models.TextField(
    _("Тестовий приватний ключ"), blank=False,  null=False, 
    default=settings.LIQPAY_SANDBOX_PRIVATE_KEY,
  )
  sandbox_mode = models.BooleanField(
    verbose_name=_("Тестовий режим"), default=settings.LIQPAY_SANDBOX_MODE,
  )
  
  @classmethod
  def modeltranslation_fields(cls):
      return []
  
  class Meta:
    verbose_name        = _('налаштування Liqpay')
    verbose_name_plural = verbose_name

from django.utils import timezone 


class LiqpayTransaction(models.Model):
  timestamp           = models.DateTimeField(verbose_name=_('Час'),default=timezone.now)
  action              = models.CharField(verbose_name=_('action'), max_length=255, blank=True, null=True)
  payment_id          = models.CharField(verbose_name=_('payment_id'), max_length=255, blank=True, null=True)
  status              = models.CharField(verbose_name=_('status'), max_length=255, blank=True, null=True)
  version             = models.CharField(verbose_name=_('version'), max_length=255, blank=True, null=True)
  type                = models.CharField(verbose_name=_('type'), max_length=255, blank=True, null=True)
  paytype             = models.CharField(verbose_name=_('paytype'), max_length=255, blank=True, null=True)
  public_key          = models.CharField(verbose_name=_('public_key'), max_length=255, blank=True, null=True)
  acq_id              = models.CharField(verbose_name=_('acq_id'), max_length=255, blank=True, null=True)
  order_id            = models.CharField(verbose_name=_('order_id'), max_length=255, blank=True, null=True)
  liqpay_order_id     = models.CharField(verbose_name=_('liqpay_order_id'), max_length=255, blank=True, null=True)
  description         = models.CharField(verbose_name=_('description'), max_length=255, blank=True, null=True)
  sender_phone        = models.CharField(verbose_name=_('sender_phone'), max_length=255, blank=True, null=True)
  sender_first_name   = models.CharField(verbose_name=_('sender_first_name'), max_length=255, blank=True, null=True)
  sender_last_name    = models.CharField(verbose_name=_('sender_last_name'), max_length=255, blank=True, null=True)
  sender_card_mask2   = models.CharField(verbose_name=_('sender_card_mask2'), max_length=255, blank=True, null=True)
  sender_card_bank    = models.CharField(verbose_name=_('sender_card_bank'), max_length=255, blank=True, null=True)
  sender_card_type    = models.CharField(verbose_name=_('sender_card_type'), max_length=255, blank=True, null=True)
  sender_card_country = models.CharField(verbose_name=_('sender_card_country'), max_length=255, blank=True, null=True)
  ip                  = models.CharField(verbose_name=_('ip'), max_length=255, blank=True, null=True)
  amount              = models.CharField(verbose_name=_('amount'), max_length=255, blank=True, null=True)
  currency            = models.CharField(verbose_name=_('currency'), max_length=255, blank=True, null=True)
  sender_commission   = models.CharField(verbose_name=_('sender_commission'), max_length=255, blank=True, null=True)
  receiver_commission = models.CharField(verbose_name=_('receiver_commission'), max_length=255, blank=True, null=True)
  agent_commission    = models.CharField(verbose_name=_('agent_commission'), max_length=255, blank=True, null=True)
  amount_debit        = models.CharField(verbose_name=_('amount_debit'), max_length=255, blank=True, null=True)
  amount_credit       = models.CharField(verbose_name=_('amount_credit'), max_length=255, blank=True, null=True)
  commission_debit    = models.CharField(verbose_name=_('commission_debit'), max_length=255, blank=True, null=True)
  commission_credit   = models.CharField(verbose_name=_('commission_credit'), max_length=255, blank=True, null=True)
  currency_debit      = models.CharField(verbose_name=_('currency_debit'), max_length=255, blank=True, null=True)
  currency_credit     = models.CharField(verbose_name=_('currency_credit'), max_length=255, blank=True, null=True)
  sender_bonus        = models.CharField(verbose_name=_('sender_bonus'), max_length=255, blank=True, null=True)
  amount_bonus        = models.CharField(verbose_name=_('amount_bonus'), max_length=255, blank=True, null=True)
  mpi_eci             = models.CharField(verbose_name=_('mpi_eci'), max_length=255, blank=True, null=True)
  is_3ds              = models.CharField(verbose_name=_('is_3ds'), max_length=255, blank=True, null=True)
  language            = models.CharField(verbose_name=_('language'), max_length=255, blank=True, null=True)
  create_date         = models.CharField(verbose_name=_('create_date'), max_length=255, blank=True, null=True)
  end_date            = models.CharField(verbose_name=_('end_date'), max_length=255, blank=True, null=True)
  transaction_id      = models.CharField(verbose_name=_('transaction_id'), max_length=255, blank=True, null=True)

  def __str__(self):
    return f'{self.order_id}|{self.amount}|{self.currency}'

  class Meta: 
    verbose_name = _('трансзакція liqpay')
    verbose_name_plural = _('трансзакції liqpay') 

