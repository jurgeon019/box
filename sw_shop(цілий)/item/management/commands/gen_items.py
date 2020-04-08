from django.core.management.base import BaseCommand
from box.sw_shop.item.models import (
  Item, ItemImage, ItemCategory, ItemFeature
)
import random
import datetime 
import json 
import csv




class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    amount = ItemCategory.objects.all().count()
    last_item = Item.objects.all().last()
    if last_item:
      i = last_item.id + 1
    else:
      i = 0
    while True:
      i += 1
      s = f'product_{i}'
      item, _ = Item.objects.get_or_create(
          slug=s,
      )
      ItemImage.objects.create(
        item=item
      )
      item.title = s
      item.category = ItemCategory.objects.get(id=random.randint(1, amount))
      # item.images.add(item_image)
      item.description = s+'sdsfsssssssssssssssssssssssssssssssssssssssssssssssssssssssssssdfsdsf'
      item.save()
    self.stdout.write(self.style.SUCCESS('Data imported successfully'))

