"""
Не можна склєювати магазин, бо на модулях тримається розділ в адмінці. 
Якшо склеїти магазин, то склеяться і моделі в адмінці.
"""


from django import apps 
from django.utils.translation import gettext_lazy as _

class ShopConfig(apps.AppConfig):
    name = 'box.apps.sw_shop'
    verbose_name = _('Магазин')
    verbose_name_plural = verbose_name


default_app_config = 'box.apps.sw_shop.ShopConfig'


