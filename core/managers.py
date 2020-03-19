from django.db import models 


__all__ = [
	"BasicManager",
]




class BasicManager(models.Manager):
	use_for_related_fields = True
	def all(self):
		return super().get_queryset().filter(is_active=True).order_by('order')

