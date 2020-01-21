from django.db import models 




class Payment(models.Model):
  order               = models.OneToOneField('order.Order', verbose_name='Заказ',on_delete=models.CASCADE, blank=True, null=True)
  status              = models.CharField(max_length=120, blank=True, null=True)
  ip                  = models.CharField(max_length=120, blank=True, null=True)
  amount              = models.CharField(max_length=120, blank=True, null=True)
  currency            = models.CharField(max_length=120, blank=True, null=True)
  sender_phone        = models.CharField(max_length=120, blank=True, null=True)
  sender_first_name   = models.CharField(max_length=120, blank=True, null=True)
  sender_last_name    = models.CharField(max_length=120, blank=True, null=True)
  sender_card_mask2   = models.CharField(max_length=120, blank=True, null=True)
  sender_card_bank    = models.CharField(max_length=120, blank=True, null=True)
  sender_card_type    = models.CharField(max_length=120, blank=True, null=True)
  sender_card_country = models.CharField(max_length=120, blank=True, null=True)
  timestamp           = models.DateTimeField(verbose_name='Время',auto_now_add=True, blank=True, null=True)

  def __str__(self):
    return f'{self.order}|{self.amount}|{self.currency}'

  class Meta: 
    verbose_name = 'Оплата'
    verbose_name_plural = 'Оплати' 

