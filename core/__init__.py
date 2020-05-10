from django import apps
from django.utils.translation import gettext_lazy as _


class CoreConfig(apps.AppConfig):
    name = 'box.core'
    verbose_name = _('Ядро')
    verbose_name_plural = verbose_name
    def ready(self):
        from .signals import handle_slug
        from .models import AbstractPage
        from django.db.models.signals import pre_save 
        pre_save.connect(handle_slug, sender=AbstractPage)




default_app_config = 'box.core.CoreConfig'


