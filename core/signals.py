from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver 
from django.utils.text import slugify

from transliterate import translit
from django.utils.text import slugify



def generate_unique_code(items, code):
	while items.filter(code=code).exists():
		code += 1 
	return code 


def generate_unique_slug(items, slug):
	origin_slug = slug
	numb = 1
	while items.filter(slug=slug).exists():
		slug = f'{origin_slug}-{numb}'
		numb += 1


def trans_slug(instance):
	from transliterate.exceptions import LanguagePackNotFound, LanguageDetectionError
	try:
		slug = slugify(translit(instance.title, reversed=True))
	except Exception as e:
		slug = slugify(instance.title)
	except Exception as e:
		slug = instance.id
	return slug 


# @receiver(post_save, sender=BaseMixin, dispatch_uid="create_code")
def handle_code(sender, instance, **kwargs):
	created = kwargs['created']
	items   = instance._meta.model.objects.all()
	if created:
		if instance.code:
			code = instance.code
		elif not instance.code:
			code = instance.id
		instance.code = generate_unique_code(items, code) 
		instance.save()
	elif not created:
		if instance.code:
			'do nothing, because instance code already exists and it is already unique'
		elif not instance.code:
			raise Exception('YOU MUST PROVIDE "code" IN ORDER TO SUCCESSFULLY UPDATE ITEM')


def handle_slug(sender, instance, **kwargs):
	created = kwargs['created']
	items   = instance._meta.model.objects.all()
	if created:
		if instance.slug:
			# slug = trans_slug(instance)
			slug = instance.slug 
		elif not instance.slug:
			# slug = instance.id 
			slug = trans_slug(instance)
		instance.slug = generate_unique_slug(items, slug)
		instance.save()
	elif not created:
		if instance.slug:
			'do nothing, because instance slug already exists and it is already unique'
		elif not instance.slug:
			raise Exception('YOU MUST PROVIDE "slug" IN ORDER TO SUCCESSFULLY UPDATE ITEM')


