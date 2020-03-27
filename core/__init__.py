<<<<<<< HEAD
from django import apps
from django.utils.translation import gettext_lazy as _


class CoreConfig(apps.AppConfig):
    name = 'box.core'
    verbose_name = _('Ядро')
    verbose_name_plural = verbose_name
    def ready(self):
        from .signals import post_save, handle_code
        from box.shop.item.models import (
            Item, ItemCategory, ItemBrand,  
            ItemCurrency,
        )
        from box.blog.models import (
            Post, PostCategory,
        )
        post_save.connect(receiver=handle_code, sender=Item)
        post_save.connect(receiver=handle_code, sender=ItemCategory)
        post_save.connect(receiver=handle_code, sender=ItemBrand)
        post_save.connect(receiver=handle_code, sender=ItemCurrency)
        post_save.connect(receiver=handle_code, sender=Post)
        post_save.connect(receiver=handle_code, sender=PostCategory)



default_app_config = 'box.core.CoreConfig'



=======
>>>>>>> a4d5039198efa087a744d65d8decd13b37be8dfc
