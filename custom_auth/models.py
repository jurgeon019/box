from django.db import models 
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
  phone_number = models.CharField(verbose_name=_("Номер телефону"), max_length=255, blank=True, null=True)
  group        = models.ForeignKey(verbose_name=_("Група"), to="customer.CustomerGroup", blank=True, null=True, on_delete=models.SET_NULL, help_text=("Група з купонами на скидку"))
  address      = models.TextField(verbose_name=_("Адреса"), blank=True, null=True)

  def __str__(self):
    return f"{self.username}, {self.get_full_name()}"
    return f"{self.first_name} {self.last_name} ({self.username}, {self.phone_number}, {self.email})"

  class Meta:
    verbose_name = _('користувач')
    verbose_name_plural = _('Список користувачів')


