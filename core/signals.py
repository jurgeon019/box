from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver 
from django.utils.text import slugify

from transliterate import translit
from django.utils.text import slugify



def generate_unique_code(items, code):
	while items.filter(code=code).exists():
		code += 1 
	return code 


def generate_unique_slug(instance, slug):
	items   = instance._meta.model.objects.all()
	origin_slug = slug
	numb = 1
	while items.filter(slug=slug).exclude(pk=instance.pk).exists():
		slug = f'{origin_slug}-{numb}'
		numb += 1
	return slug 


def trans_slug(instance):
	from transliterate.exceptions import LanguagePackNotFound, LanguageDetectionError
	try:
		slug = slugify(translit(instance.title, reversed=True))
	except Exception as e:
		slug = slugify(instance.title)
	# except Exception as e:
	# 	slug = instance.id
	return slug 

def handle_slug(instance):
	if instance.slug:
		# slug = trans_slug(instance)
		# slug = trans_slug(instance.slug) # TODO: try it 
		slug = instance.slug 
	elif not instance.slug:
		slug = trans_slug(instance)
	# if instance.code:
	# 	code = instance.code
	# elif not instance.code and instance.id:
	# 	code = instance.id
	# else:
	# 	print('?????????????')
	# 	raise Exception('dafuk are you doing man?')
	# instance.code = generate_unique_code(items, code) 
	instance.slug = generate_unique_slug(instance, slug)
	return instance



def page_post_save(sender, instance, **kwargs):
	created = kwargs['created']
	if created:
		instance = handle_slug(instance)
		instance.save()

	# elif not created:
	# 	if instance.slug:
	# 		'do nothing, because instance slug already exists and it is already unique'
	# 	elif not instance.slug:
	# 		raise Exception('YOU MUST PROVIDE "slug" IN ORDER TO SUCCESSFULLY UPDATE ITEM')
	# 	# if instance.code:
	# 	# 	'do nothing, because instance code already exists and it is already unique'
	# 	# elif not instance.code:
	# 	# 	raise Exception('YOU MUST PROVIDE "code" IN ORDER TO SUCCESSFULLY UPDATE ITEM')


