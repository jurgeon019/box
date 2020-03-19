from django.core.paginator import Paginator


def paginate_items_to_template(query, slug):
    return items 


def generate_unique_slug(klass, field, item, *args, **kwargs):
	origin_slug = slugify(translit(field, reversed=True)) # slugify(field)
	unique_slug = origin_slug
	numb = 1
	obj = klass.objects.filter(slug=unique_slug)
	while obj.exists():
		obj = obj.first()
		unique_slug = f'{origin_slug}-{numb}'
		numb += 1
	return unique_slug


def item_image_folder(instance, filename):
	ext = filename.split('.')[-1]

	# foldername = instance.slug
	foldername = 'slug'

	# slug = instance.slug
	slug = 'slug'

	filename = slug + '.' + ext

	path = f"shop/items"
	path = '/'.join(['shop','items'])

	path = f"{foldername}/{filename}"
	path = '/'.join([foldername, filename])

	path = f"shop/items/{foldername}/{filename}"
	path = '/'.join(['shop', 'items', foldername, filename])

	return path 

