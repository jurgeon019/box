from django.core.management.base import BaseCommand
from box.apps.sw_shop.sw_catalog.models import ItemCategory

import csv 

class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    filenames = ['all_categories_.csv', 'all_categories.csv']
    for filename in filenames:
      categories = [dct for dct in map(dict, csv.DictReader(open(filename)))]
      for category in categories:
        title = category['Заголовок']
        title_uk = category['Заголовок_uk']
        title_ru = category['Заголовок_ru']
        try:
          cat = ItemCategory.objects.get(
            title__iexact=title.lower().strip()
          )
          cat.slug = cat.slug 
          cat.title_uk = title_uk
          cat.title_ru = title_ru
          cat.save()
          print(cat)
        except Exception as e:
          # print(e)
          pass 
    self.stdout.write(self.style.SUCCESS('Data imported successfully'))

