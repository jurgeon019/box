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
    headers_row = list_file[0]
    items_rows  = list_file[1:] 
    feature_name_indexes  = [i for i, o in enumerate(headers_row) if o=='Название_Характеристики']
    feature_value_indexes = [i for i, o in enumerate(headers_row) if o=='Значение_Характеристики']
    # feature_code_indexes  = [i for i, o in enumerate(headers_row) if o=='feature_code']
    items_features = []
    item_features_names  = []
    item_features_values = []
    # item_features_codes  = []
    features = []
    
    for item_row in items_rows:
      for i in feature_name_indexes:
        item_features_names.append(item_row[i])
      for i in feature_value_indexes:
        item_features_values.append(item_row[i])
      # for i in feature_code_indexes:
      #   item_features_codes.append(item_row[i])

      features = dict(zip(item_features_names, item_features_values))

      # TODO: допиляти так, шоб можна було в ексель-файл записувати 
      # крім назви характеристики і значення характеристики, ще й код 
      # характеристики і батьківську категорію
      # for i in range(len(item_features_names)):
      #   features.append({
      #     'feature_name': ,
      #     '':,
      #     '':,
      #     '':,
      #   })

      items_features.append(features) 

    for i in range(len(items_features)):
      dict_items[i]['features'] = items_features[i]


    for item in dict_items:
      # print(item)

      # if Item.objects.filter(slug=item['Ссылка']).exists():
      #   print(f"Item with slug `{item['Ссылка']}` already exists")

      # if Item.objects.filter(code=item['Артикул']).exists():
      #   print(f"Item with code `{item['Артикул']}` already exists")
      
      # else:
      if True:
        try:
          new_item, _          = Item.objects.get_or_create(
            slug = item['Ссылка'],
          )
          new_item.meta_descr  = item["Мета_Описание"]
          new_item.meta_title  = item["Мета_Заголовок"]
          new_item.title       = item["Заголовок"]
          new_item.description = item["Описание"]
          new_item.code        = item["Артикул"]
          new_item.old_price   = item["Старая_Цена"]
          new_item.new_price   = item["Новая_Цена"]
          category = ItemCategory.objects.filter(slug__iexact=item["Категория"].lower())
          if category:
            print(category)
            category = category.first() 
            new_item.category    = category
          # new_item.currency    = item['Валюта']
          # new_item.in_stock    = item["В_Наличии"]
          # new_item.is_new      = item["Новое"]
          # new_item.is_active   = item["Активен"]
          new_item.save()
          for image in item['Изображения'].split(','):
            print(image)
            image = ItemImage.objects.create(
              image = f'shop/items/{image.strip()}',
              item  =  new_item, 
            )
          
          # for k, v in item['features'].items():
          #   new_feature, _ = ItemFeature.objects.get_or_create(
          #     item = new_item, 
          #     name =k,
          #     value=v,
          #   )
          #   # new_item.features.add(new_feature)
          #   print(new_feature.id, new_feature.name)
          #   print(new_item.id ,new_item.title)
          new_item.save()
        except Exception as e:
          print('[ERROR]: ', e)
    self.stdout.write(self.style.SUCCESS('Data imported successfully'))

