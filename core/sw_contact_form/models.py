from django.db import models 
from django.utils.translation import gettext_lazy as _



class Contact(models.Model):
    name    = models.CharField(
        verbose_name=_('Імя'), blank=True, null=True, max_length=255
    )
    email   = models.EmailField(
        verbose_name=_('Email'), blank=True, null=True, max_length=255
    )
    phone   = models.CharField(
        verbose_name=_('Телефон'), blank=True, null=True, max_length=255
    )
    message = models.TextField(
        verbose_name=_('Текст'), blank=True, null=True
    )
    note    = models.TextField(
        verbose_name=_('Примітки адміністратора'), blank=True, null=True
    )
    url     = models.CharField(
        verbose_name=_('Ссилка'), blank=True, null=True, max_length=255, 
        help_text=_("Ссилка на сторінку, з якої було відправлено контактну форму")
    )
    checked = models.BooleanField(
        verbose_name=_("Оброблено"), default=False
    )

    def __str__(self):
        return f"{self.name}, {self.email}, {self.phone}, {self.message}"

    class Meta:
        verbose_name = _('Зворотний звязок')
        verbose_name_plural = verbose_name

