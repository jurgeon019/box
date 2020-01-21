from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify

from transliterate import translit

from .models import Item


def post_save_item_slug(sender, instance, *args, **kwargs):
  if not instance.slug:
    try:
      slug = slugify(translit(instance.title, reversed=True))
    except:
      slug = slugify(instance.title)
    instance.slug = slug + str(instance.id)
    instance.save()


