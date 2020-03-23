from django.utils.translation import gettext_lazy as _
from django.db import models 
from django.contrib.auth.models import AbstractUser


class AbstractBoxUser(AbstractUser):
  gender_choices = [
    ["u",_("Невідомо")],
    ["m",_("Чоловік")],
    ["f",_("Жінка")],
  ]
  group        = models.ForeignKey(verbose_name=_("Група"), to="customer.CustomerGroup", blank=True, null=True, on_delete=models.SET_NULL, help_text=("Група з купонами на скидку"))
  phone_number = models.CharField(verbose_name=_("Номер телефону"), max_length=255, blank=True, null=True)
  address      = models.TextField(verbose_name=_("Адреса"), blank=True, null=True)
  birth_date   = models.DateTimeField(verbose_name=_("Дата народження"), blank=True, null=True)
  gender       = models.CharField(verbose_name=_("Стать"), choices=gender_choices, max_length=20, default=0)

  def __str__(self):
    return f"{self.username}, {self.get_full_name()}"
    return f"{self.first_name} {self.last_name} ({self.username}, {self.phone_number}, {self.email})"

  class Meta:
    abstract = True 


class BoxUser(AbstractBoxUser):
  class Meta:
    verbose_name = _('користувач')
    verbose_name_plural = _('Список користувачів')

