from django.core.management.base import BaseCommand
from shop.item.models import (
  Item, ItemImage, ItemCategory, ItemFeature
)
import random
import datetime
import json
import csv



class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument(
      'file_name',
      type=str,
      help='File, that contains the main item\'s information'
    )
  def handle(self, *args, **kwargs):
    dict_file   = map(dict, csv.DictReader(open(f"{kwargs['file_name']}")))
    dict_items  = [dct for dct in dict_file]
    list_file   = list(csv.reader(open(f"{kwargs['file_name']}")))
    print(list_file)
    headers_row = list_file[0]
    for item in dict_items:
      if Item.objects.filter(slug=item['slug']).exists():
        slug = item['slug']
        self.stdout.write(self.style.SUCCESS(f"Item with slug `{slug}` already exists"))
      else:
        try:
          new_category, _ = ItemCategory.objects.get_or_create(
            slug   = item["slug"],
            title = item["title"],
            parent = ItemCategory.objects.filter(slug=item["parent"]).first(),
          )
          # new_category.title  = title
          # new_category.parent = parent
          new_category.save()
          print(new_category)
        except Exception as e:
          print('[ERROR]: ', e)
    self.stdout.write(self.style.SUCCESS('Data imported successfully'))
