from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver 
from django.utils.text import slugify

from transliterate import translit
from django.utils.text import slugify



def generate_unique_slug(instance, slug):
	items   = instance._meta.model.objects.all()
	origin_slug = slug
	numb = 1
	while items.filter(slug=slug).exclude(pk=instance.pk).exists():
		slug = f'{origin_slug}-{numb}'
		numb += 1
	return slug 


def trans_slug(instance):
	try:
		slug = slugify(translit(instance.title, reversed=True))
	except Exception as e:
		slug = slugify(instance.title)
	return slug 


def handle_slug(instance, *args, **kwargs):
	if instance.slug:
		slug = instance.slug 
	elif not instance.slug:
		slug = trans_slug(instance)
	instance.slug = generate_unique_slug(instance, slug)
	return instance



