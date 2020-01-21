from django import apps 
from django.utils.translation import ugettext_lazy as _


class ProfileConfig(apps.AppConfig):
    name = 'shop.profile'
    verbose_name = _('Кабінет користувача')
    