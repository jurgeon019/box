from django import apps
from django.utils.translation import gettext_lazy as _


class CoreConfig(apps.AppConfig):
    name = 'box.core'
    verbose_name = _('Ядро')
    verbose_name_plural = verbose_name
    # def ready(self):
    #     from .signals import post_save, page_post_save
    #     from box.shop.item.models import (
    #         Item, ItemCategory, ItemBrand,  
    #     )
    #     from box.blog.models import (
    #         Post, PostCategory,
    #     )
    #     models = [
    #         # Item,
    #         # ItemCategory,
    #         # ItemBrand,
    #         # Post,
    #         # PostCategory,
    #     ]
    #     for model in models:
    #         post_save.connect(receiver=page_post_save, sender=model)



default_app_config = 'box.core.CoreConfig'



