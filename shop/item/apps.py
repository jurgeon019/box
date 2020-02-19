from django.apps import AppConfig



class ItemConfig(AppConfig):
    name = 'box.shop.item'
    verbose_name = 'магазин'
    def ready(self):
        from .models import Item 
        # from .signals import post_save_item_slug, post_save
        # post_save.connect(post_save_item_slug, sender=Item)

