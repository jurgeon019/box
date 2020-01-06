from django.db import models 
from shop.item.models import Item 
from django.utils import timezone


class CreditRequest(models.Model): 
    item  = models.ForeignKey(verbose_name=("Товар"),  to='item.Item', blank=True, null=True, on_delete=models.CASCADE, related_name='credits')
    name  = models.CharField(verbose_name=("Ім'я"),    max_length=120, blank=True, null=True)
    email = models.CharField(verbose_name=("Емайл"),   max_length=120, blank=True, null=True)
    phone = models.CharField(verbose_name=("Телефон"), max_length=120, blank=True, null=True)
    created = models.DateTimeField(verbose_name=("Створено"), blank=True, null=True, default=timezone.now)
    def __str__(self):
        return f"{self.name}, {self.email}, {self.phone}"
    
    class Meta:
        verbose_name = 'Заявка на кредит'
        verbose_name_plural = 'Заявки на кредит'


class ContactRequest(models.Model):
    name    = models.CharField(verbose_name=("Ім'я"),         max_length=120, blank=True, null=True)
    phone   = models.CharField(verbose_name=("Телефон"),      max_length=120, blank=True, null=True)
    email   = models.CharField(verbose_name=("Емайл"),        max_length=120, blank=True, null=True)
    message = models.TextField(verbose_name=("Повідомлення"), blank=True, null=True)
    created = models.DateTimeField(verbose_name=("Створено"), blank=True, null=True, default=timezone.now)
    def __str__(self):
        return f"{self.name}, {self.email}, {self.phone}"

    class Meta:
        verbose_name = 'Контакти'
        verbose_name_plural = 'Контакти'


class OrderRequest(models.Model):
    name    = models.CharField(verbose_name=("Ім'я"),         max_length=120, blank=True, null=True)
    phone   = models.CharField(verbose_name=("Телефон"),      max_length=120, blank=True, null=True)
    email   = models.CharField(verbose_name=("Емайл"),        max_length=120, blank=True, null=True)
    message = models.TextField(verbose_name=("Повідомлення"), blank=True, null=True)
    created = models.DateTimeField(verbose_name=("Створено"), blank=True, null=True, default=timezone.now)
    item    = models.ForeignKey(verbose_name=("Товар"), to="item.Item", blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}, {self.email}, {self.phone}"

    class Meta:
        verbose_name = 'Покупка в один клік'
        verbose_name_plural = 'покупки в 1 клік'





