from django.db import transaction

from box.shop.item.models import *
import csv
import pandas as pd 
from io import StringIO
from django.conf import settings 



BASE_DIR = settings.BASE_DIR 

count = 0

def get_family_tree(child):
  subcategories = child.subcategories.all()
  if not subcategories:
      return {
        "title": child.title, 
        "slug":child.slug,
        "items_count":"",
        "subcategories": []
      }
  return {
      "title": child.title,
      "slug":child.slug,
      "subcategories": [get_family_tree(child) for child in subcategories],
  }


def get_subcategories_count(child):
  subcategories = child.subcategories.all()
  if not subcategories:
      return {
        "title": child.title, 
        "slug":child.slug,
        "items_count":"",
        "subcategories": []
      }
  return {
      "title": child.title,
      "slug":child.slug,
      "subcategories": [get_family_tree(child) for child in subcategories],
  }




def read_items_from_xlsx_admin(filename):
  print(filename)
  print(type(filename))
  items      = pd.read_excel(filename, sheet_name="Товары")
  items      = items.to_csv()
  categories = pd.read_excel(filename, sheet_name="Категории")
  categories = categories.to_csv()
  create_categories(
    [dct for dct in map(dict, csv.DictReader(StringIO(categories)))],
    list(csv.reader(StringIO(categories)))
  )
  create_items(
    [dct for dct in map(dict, csv.DictReader(StringIO(items)))], 
    list(csv.reader(StringIO(items)))
  )
  return True


def read_items_from_xlsx(filename):
  items      = pd.read_excel(filename, sheet_name="Товары")
  items      = items.to_csv()
  categories = pd.read_excel(filename, sheet_name="Категории")
  categories = categories.to_csv()
  create_categories(
    [dct for dct in map(dict, csv.DictReader(StringIO(categories)))],
    list(csv.reader(StringIO(categories)))
  )
  create_items(
    [dct for dct in map(dict, csv.DictReader(StringIO(items)))], 
    list(csv.reader(StringIO(items)))
  )
  return True


def read_items_from_csv(filename):
  create_items(
    [dct for dct in map(dict, csv.DictReader(open(filename)))], 
    list(csv.reader(open(filename))),
  )
  return True 


def read_categories_from_csv(filename):
  create_categories(
    [dct for dct in map(dict, csv.DictReader(open(filename)))],
    list(csv.reader(open(filename))),
  )
  return True 


def create_items(dict_file, list_file):
  items       = dict_file
  headers_row = list_file[0]
  items_rows  = list_file[1:] 
  feature_name_indexes  = [i for i, o in enumerate(headers_row) if "Название_Характеристики" in o]
  feature_value_indexes = [i for i, o in enumerate(headers_row) if "Значение_Характеристики" in o]
  # feature_code_indexes  = [i for i, o in enumerate(headers_row) if "feature_code" in o]
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
    # TODO: допиляти так, шоб можна було в ексель-файл записувати 
    # крім назви характеристики і значення характеристики, ще й код 
    # характеристики і батьківську категорію
    # for i in range(len(item_features_names)):
    #   features.append({
    #     "feature_name": ,
    #     "":,
    #     "":,
    #     "":,
    #   })
    features = dict(zip(item_features_names, item_features_values))
    items_features.append(features) 

  for i in range(len(items_features)):
    items[i]["features"] = items_features[i]
  
  for item in items:
      category_slug = item["Категория"].lower()
      item_slug     = item["Ссылка"]
      new_item, _          = Item.objects.get_or_create(
        slug = item_slug,
      )
      new_item.meta_descr  = item["Мета_Описание"]
      new_item.meta_title  = item["Мета_Заголовок"]
      new_item.meta_key    = item["Мета_Ключевые_Слова"]
      new_item.title       = item["Заголовок"]
      new_item.description = item["Описание"]
      new_item.code        = item["Артикул"]
      new_item.old_price   = item["Старая_Цена"]
      new_item.new_price   = item["Новая_Цена"]
      # new_item.currency    = item["Валюта"]
      # new_item.in_stock    = item["В_Наличии"]
      # new_item.is_new      = item["Новое"]
      # new_item.is_active   = item["Активен"]
      new_item.category = ItemCategory.objects.get(slug__iexact=category_slug)

      for image in item["Изображения"].split(","):
        print(image)
        image = ItemImage.objects.create(
          image = f"shop/items/{image.strip()}",
          item  =  new_item, 
        )
      new_item.save()
      new_item.create_thumbnail_from_images()
      
      for k, v in item["features"].items():
        new_feature, _ = ItemFeature.objects.get_or_create(
          item = new_item, 
          name =k,
          value=v,
        )
        print(new_feature.id, new_feature.name)
      new_item.save()
      print(new_item.id ,new_item.title)


def create_categories(dict_file, list_file):
  for item in dict_file:
    try:
      title       = item["title"]
      slug        = item["slug"]
      parent_slug = item["parent"]
      image       = item['image']
      image_name  = image.split('/')[-1]

      with transaction.atomic():
        new_category, _ = ItemCategory.objects.get_or_create(
          slug = slug,
        )
        new_category.title  = title
        parent      = ItemCategory.objects.filter(slug=parent_slug).first()
        new_category.parent = parent
        new_category.thumbnail = 'shop/categories/' + image
        new_category.save()
        print(new_category)
    except Exception as e:
      print("[ERROR]: ", e)
  return True 




















