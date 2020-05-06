from django.db import models 
from django.utils.translation import gettext_lazy as _

from box.core.models import AbstractRecipientEmail

from box.core.sw_solo.models  import SingletonModel


class ContactConfig(SingletonModel):
    class Meta:
        verbose_name=_("Налаштування зворотнього звязку")
        verbose_name_plural = verbose_name


class ContactRecipientEmail(AbstractRecipientEmail):
    config = models.ForeignKey(
        to="sw_contact_form.ContactConfig", related_name=_("emails"), 
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("емейл для сповіщень про контактні форми")
        verbose_name_plural = _("емейли для сповіщень про контактні форми")


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

