from django.db import models 


__all__ = [
	'BasicManager',
	'ActiveManager',
]




class BasicManager(models.Manager):
	# use_for_related_fields = True
	def all(self):
		return super().get_queryset().order_by('order')


class ActiveManager(models.Manager):
	use_for_related_fields = True 
	# TODO: розібратись з related_name filtering
	def all(self):
		return super().get_queryset().order_by('order').filter(is_active=True)



