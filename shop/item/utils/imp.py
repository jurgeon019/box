from django.conf import settings 
from django.db import transaction

from box.shop.item.models import *

from io import StringIO
import pandas as pd 
import csv


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


read_items_from_xlsx


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
      create_item(item)


def create_item(item):
  # new_item.in_stock    = item["В_Наличии"]
  # new_item.is_new      = item["Новое"]
  # new_item.is_active   = item["Активен"]
  category_slug = item["Категория"].lower()
  item_slug     = item["Ссылка"]
  new_item, _          = Item.objects.get_or_create(
    slug = item_slug,
  )
  slugs = ItemCategory.objects.all().values_list('slug')
  if settings.MULTIPLE_CATEGORY:
    new_item.categories.add(ItemCategory.objects.get(slug__iexact = category_slug))
  else:
    new_item.category = ItemCategory.objects.get(slug__iexact=category_slug)
  new_item.meta_descr  = item["Мета_Описание"]
  new_item.meta_title  = item["Мета_Заголовок"]
  new_item.meta_key    = item["Мета_Ключевые_Слова"]
  new_item.title       = item["Заголовок"]
  new_item.description = item["Описание"]
  new_item.code        = item["Артикул"]
  new_item.old_price   = item["Старая_Цена"]
  new_item.new_price   = item["Новая_Цена"]
  currency             = item['Валюта']
  new_item.currency, _ = Currency.objects.get_or_create(name=currency)
  images = item["Изображения"]
  if images:
    images = images.split(",")
    for image in images:
      # print(image)
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
  new_item.save()


def create_categories(dict_file, list_file):
  for item in dict_file:
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
  return True 


def import_items_from_xml_by_xmljson(filename):
  from xmljson import badgerfish as bf
  from xml.etree.ElementTree import fromstring
  import json 
  items = '<p id="main">Hello<b>bold</b></p>'
  items = open(filename).read()
  items = bf.data(fromstring(items))
  items = json.dumps(items)
  items = json.loads(items)
  items = items['objects']['object']
  for item in items:
    fields = item['field']
    import pprint; pprint.pprint(fields)


class XMLItem(object):
  meta_title  = None
  meta_descr  = None
  meta_key    = None
  title       = None
  description = None
  code        = None
  slug        = None
  thumbnail   = None
  old_price   = None
  new_price   = None
  currency    = None
  category    = None
  in_stock    = None
  is_new      = None
  is_active   = None
  created     = None
  updated     = None
  order       = None
  fields      = {}

  def __str__(self):
    return f'{self.fields}'


def import_items_from_xml_by_xml_etree(filename):
  import xml.etree.ElementTree as ET
  # *******
  # tree = ET.parse(filename)
  # xml_data = tree.getroot()W
  # xmlstr = ET.tostring(xml_data, encoding='utf8', method='xml')
  # data_dict = dict(xmltodict.parse(xmlstr))
  # print(data_dict)
  # with open('new_data_2.json', 'w+') as json_file:
  #     json.dump(data_dict, json_file, indent=4, sort_keys=True)
  # *******
  # https://stackoverflow.com/questions/45144645/parsing-xml-file-in-django


  tree = ET.parse(filename)
  root = tree.getroot()
  for att in root:
    fields = att.findall('field')#.text
    item = Item() 

    xml_item = XMLItem()
    for field in fields:
      name  = field.get('name')
      descr = field.get('descr')
      text  = field.text
      xml_item.fields.update({name:text})
      # setattr(xml_item, name, text)
    print(xml_item)

    title       = xml_item.fields['title']
    meta_title  = xml_item.fields['meta_title']
    meta_descr  = xml_item.fields['meta_descr']
    meta_key    = xml_item.fields['meta_key']
    title       = xml_item.fields['title']
    description = xml_item.fields['description']
    code        = xml_item.fields['code']
    slug        = xml_item.fields['slug']
    thumbnail   = xml_item.fields['thumbnail']
    old_price   = xml_item.fields['old_price']
    new_price   = xml_item.fields['new_price']
    currency    = xml_item.fields['currency']
    category    = xml_item.fields['category']
    in_stock    = xml_item.fields['in_stock']
    is_new      = xml_item.fields['is_new']
    is_active   = xml_item.fields['is_active']
    created     = xml_item.fields['created']
    updated     = xml_item.fields['updated']
    order       = xml_item.fields['order']
    print(xml_item.fields)
    return '123'



    # currency = Currency.objects.get()


    item.meta_title  = meta_title
    item.meta_descr  = meta_descr
    item.meta_key    = meta_key
    item.title       = title
    item.description = description
    item.code        = code
    item.slug        = slug
    item.thumbnail   = thumbnail
    item.old_price   = old_price
    item.new_price   = new_price
    item.currency    = currency
    item.category    = category
    item.in_stock    = in_stock
    item.is_new      = is_new
    item.is_active   = is_active
    item.created     = created
    item.updated     = updated
    item.order       = order
    # item.save()


def import_items_from_xml_by_xmltodict(filename):
  import xmltodict
  import json

  items = xmltodict.parse(open(filename).read())
  items = json.dumps(items)
  items = json.loads(items)
  items = items['objects']['object']
  for item in items:
    fields = item['field']
    for field in fields:
      item = Item()
      text = field.get('#text')
      name = field['@name']
      setattr(item, name, text)
      # item.save()
      print(item)
      import pprint; pprint.pprint(field)


def import_items_from_xml(filename):
  import_items_from_xml_by_xml_etree(filename)
  return True 
