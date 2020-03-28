from django import apps
from django.utils.translation import gettext_lazy as _


class CoreConfig(apps.AppConfig):
    name = 'box.core'
    verbose_name = _('Ядро')
    verbose_name_plural = verbose_name
    def ready(self):
        from .signals import post_save, handle_code, handle_slug
        from box.shop.item.models import (
            Item, ItemCategory, ItemBrand,  
        )
        from box.blog.models import (
            Post, PostCategory,
        )
        models = [
            Item,
            ItemCategory,
            ItemBrand,
            Post,
            PostCategory,
        ]
        for model in models:
            post_save.connect(receiver=handle_code, sender=model)
            post_save.connect(receiver=handle_slug, sender=model)



default_app_config = 'box.core.CoreConfig'



