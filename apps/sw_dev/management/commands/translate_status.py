from django.core.management.base import BaseCommand
from box.apps.sw_shop.sw_catalog.models import ItemStock, Item 

import csv 

class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    filenames = ['status.csv',]
    for filename in filenames:
      categories = [dct for dct in map(dict, csv.DictReader(open(filename)))]
      for category in categories:
        text = category['Название']
        text_uk = category['Название_uk']
        text_ru = category['Название_ru']
        # for status in ItemStock.objects.all():
        #     print(status)
        # print(ItemStock.objects.get(text='Товар доступен'))
        try:
            status = ItemStock.objects.get(
                # text__iexact=text.lower().strip()
                text=text,
            )
            status.text_uk = text_uk
            status.text_ru = text_ru
            status.save()
            print(status)
        except Exception as e:
            print(e)
    reds = [
      'Немає в наявності',
      'Нет в наличии',
      'Товар не доступний',
    ]
    greens = [
      'Є в наявності',
      'Товар доступний',
      'В наявності',
    ]
    oranges = [
      'Обмежена кількість',
      'Увага: обмежена кількість товару в наявності!',
      'Під заказ',
      'Під заказ, 5 днів',
      'Під заказ, 10 днів',
      'Під заказ, 15 днів',
      'Під заказ, 30 днів',
    ]
    for status in ItemStock.objects.all():
      if status.text_uk in greens:
        status.colour  = 'g'
        # status.colour  = 'green'
      elif status.text_uk in reds:
        status.colour  = 'r'
        status.availability = False
        # status.colour  = 'red'
      elif status.text_uk in oranges or 'заказ' in status.text:
        status.colour  = 'o'
        # status.colour  = 'orange'
      status.save()
      print(status.text)
      print(status.colour)
    
    Item.objects.all().filter(in_stock__availability = False).update(amount=0)
    self.stdout.write(self.style.SUCCESS('Data imported successfully'))

