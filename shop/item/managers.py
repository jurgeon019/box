from django.db import models 


__all__ = [
    "ItemCategoryManager",
	"ImageManager",
	"ItemManager",

]



class OrderingManager(models.Manager):
	use_for_related_fields = True
	def all(self):
		return super().get_queryset().filter(is_active=True).order_by('-order','id')


class ItemCategoryManager(OrderingManager):
	pass


class ImageManager(OrderingManager):
	pass


class ItemManager(OrderingManager):
	pass
