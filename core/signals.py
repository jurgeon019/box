from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver 
from django.utils.text import slugify

from transliterate import translit




# @receiver(post_save, sender=BaseMixin, dispatch_uid="create_code")
def handle_code(sender, instance, **kwargs):
	created = kwargs['created']
	items   = instance._meta.model.objects.all()
	if created:
		if instance.code:
			'do nothing' 
		elif not instance.code:
			code = instance.id
			while items.filter(code=code).exists():
				code += 1 
			instance.code = code 
		instance.save()
	elif not created:
		'do nothing'
		if instance.code:
			'do nothing'
		elif not instance.code:
			raise Exception('YOU MUST PROVIDE "CODE" IN ORDER TO SUCCESSFULLY UPDATE ITEM')
# TODO: проверки на всех if-ах. 
# TODO: handle_slug


# def post_save_item_slug(sender, instance, *args, **kwargs):
#   if not instance.slug:
#     try:
#       slug = slugify(translit(instance.title, reversed=True))
#     except:
#       slug = slugify(instance.title)
#     instance.slug = slug + str(instance.id)
#     instance.save()
