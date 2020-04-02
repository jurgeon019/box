from django.utils.translation import gettext_lazy as _

from import_export.resources import ModelResource
from import_export.fields import Field 
from import_export.widgets import ForeignKeyWidget

import json 

from ..models import * 
from box.core.utils import get_multilingual_fields



class ItemResource(ModelResource):

    class Meta:
        model = Item 
        exclude = [
            'code',
            'created',
            'updated',
            'order',
        ]

    category  = Field(
        column_name=_('category'),
        attribute='category',
        widget=ForeignKeyWidget(ItemCategory, field='id'),
    )
    images        = Field(column_name=_('images') )
    server_images = Field(column_name=_('server_images') )
    
    features  = Field(column_name=_('features') )
    # reviews  = Field(column_name=_('reviews') )
    # variants = Field(column_name=_('variants') )
    # options  = Field(column_name=_('options') )

    # m2m 
    # similars = Field(column_name='similars')
    # markers = Field(column_name='markers')
    # markers = Field(column_name="markers", widget=ManyToManyWidget(ItemMarker))
    # markers = Field(column_name="markers", widget=ManyToManyWidget(ItemMarker, field='name'))


    def before_import_row(self, row, **kwargs):
        # self.handle_markers_import(row)
        # self.handle_similars_import(row)
        # self.handle_features_import(row)
        self.handle_category_import(row)
        self.handle_manufacturer_import(row)
        self.handle_brand_import(row)
        self.handle_currency_import(row)
        self.handle_in_stock_import(row)

    def after_import_row(self, row, row_result,**kwargs):
        print("row_result")
        print(row_result)
        self.handle_images_import(row)
        self.handle_server_images_import(row)


    def get_export_order(self):
        multilingual_fields = get_multilingual_fields(self._meta.model)
        order = [
            'id',
            'is_active',
            # 'code',
            'old_price',
            'new_price',
            "currency",
            # 'image',

            "images",
            'server_images',
            # "features",

            "category",
            "manufacturer",
            "brand",
            "in_stock",
            'amount',
            'units',
            # "markers",
            # "similars",
            # "reviews",
            # "variants",
            # "options",
            # 'slug',
            *multilingual_fields['title'],
            *multilingual_fields['description'],
            *multilingual_fields['alt'],
            *multilingual_fields['meta_title'],
            *multilingual_fields['meta_descr'],
            *multilingual_fields['meta_key'],
        ]
        return order 

    def get_import_id_fields(self):
        fields = [
            'id',
        ]
        return fields 


    def handle_manufacturer_import(self, row):
        if row.get('manufacturer'):
            manufacturer_name   = row['manufacturer']
            manufacturer, _     = ItemManufacturer.objects.get_or_create(name=manufacturer_name)
            row['manufacturer'] = manufacturer.id

    def dehydrate_manufacturer(self, item):
        manufacturer = None 
        if item.manufacturer:
            manufacturer = item.manufacturer.name
        return manufacturer


    def handle_brand_import(self, row):
        if row.get('brand'):
            brand_title  = row['brand']
            brand, _     = ItemBrand.objects.get_or_create(title=brand_title)
            row['brand'] = brand.id

    def dehydrate_brand(self, item):
        brand = None 
        if item.brand: brand = item.brand.title
        return brand
        

    def handle_currency_import(self, row):
        if row.get('currency'):
            currency_code   = row['currency']
            currency, _     = ItemCurrency.objects.get_or_create(code=currency_code)
            row['currency'] = currency.id

    def dehydrate_currency(self, item):
        currency = None
        if item.currency: currency = item.currency.code 
        return currency


    def handle_category_import(self, row):
        if row.get('category'):
            category_id = row['category']
            category, _ = ItemCategory.objects.get_or_create(id=category_id)
            row['category'] = category.id

    def dehydrate_category(self, item):
        category = None 
        if item.category: category = item.category.id 
        return category


    def handle_in_stock_import(self, row):
        if row.get('in_stock'):
            in_stock_text   = row['in_stock']
            in_stock, _     = ItemStock.objects.get_or_create(text=in_stock_text)
            row['in_stock'] = in_stock.id
            
    def dehydrate_in_stock(self, item):
        in_stock = None 
        if item.in_stock: in_stock = item.in_stock.text 
        return in_stock


    def handle_images_import(self, row):
        from box.sw_shop.item.utils.utils import get_image_path
        if row.get('images'):
            image_names = row['images'].split(',')
            print("image_names")
            print(image_names)
            images = []
            # images = [ ItemImage.objects.get_or_create(image=f'shop/item/{image_name.strip()}')[0].id for image_name in image_names]
            item = Item.objects.get(id=row['id'])
            for image_name in image_names:
                if image_name.startswith('shop/item/'):
                    # Кодова фраза, якшо вдруг захочеш протестити як виглядають картинки на сайті
                    ItemImage.objects.get_or_create(
                        item=item,
                        image=image_name,
                    )
                else:
                    ItemImage.objects.get_or_create(
                        item=item,
                        image=get_image_path(item, image_name),
                    )
    
    def dehydrate_images(self, item):
        images = ItemImage.objects.all().filter(item=item) 
        images_url = ','.join([image.image.url.split('/')[-1] for image in images])
        return images_url


    def handle_server_images_import(self, row):
        if row.get('server_images'):
            server_images = row['server_images'].split(',')
            print('server_images')
            print(server_images)
            for image in server_images:
                image = image.strip()
                # handle_image_pars(image)
                # TODO: запхати всі ссилки для парсу картинок в якись брокер задач + селері

    def dehydrate_server_images(self, item):
        from django.contrib.sites.models import Site 
        domain = Site.objects.get_current().domain
        server_images = []
        images = ItemImage.objects.all().filter(item=item)
        for image in images:
            server_image = f'https://{domain}{image.image.url}'
            server_images.append(server_image)
        return ','.join(server_images) 

        

    # def handle_features_import(self, row):
    #     if row.get('features'):
    #         features = []
    #         for feature in json.loads(row['features']):
    #             feature, _ = ItemFeature.objects.get_or_create(code=feature['code'])
    #             features.append(feature.id)
    #         row['features'] = features 

    # def dehydrate_features(self, item):
    #     features = []
    #     count = 0 # 1
    #     for feature in ItemFeature.objects.all().filter(item=item):
    #         values = [value.value for value in feature.value.all()]
    #         features.append({
    #             'id': feature.id,
    #             'code':feature.code,
    #             'name':feature.name.name,
    #             'values':values,
    #             # 'feature_value':feature.value.value,
    #         })
    #         count += 1 
    #     return features
    
    # def handle_markers_import(self, row):
    #     if row.get('markers'):
    #         markers = []
    #         for marker_name in row['markers'].split(','):
    #             marker, _ = ItemMarker.objects.get_or_create(name=marker_name)
    #             markers.append(marker.id)
    #         row['markers'] = ','.join(markers)

    # # def dehydrate_markers(self, item):
    # #     markers = None 
    # #     if item.markers:
    # #         markers = ','.join([marker.text for marker in item.markers.all()])
    # #     return markers

    # def handle_similars_import(self, row):
    #     if row.get('similars'):
    #         similars = []
    #         for pk in row['similars'].split(','):
    #             similar  = Item.objects.get(pk=pk)
    #             similars.append(similar.pk)
    #         row['similars'] = ','.join(similars)

    # # def dehydrate_similars(self, item):
    # #     similars = None 
    # #     if item.similars:
    # #         similars = item.similars.all()
    # #     return similars.values_list('code', flat=True)

    # # def dehydrate_variants(self, item):
    # #     variants = ItemVariant.objects.all().filter(item=item)
    # #     # if variants.exists:
    # #     #     return variants
    # #     # return None
    # #     return variants.values_list('code', flat=True)    
    # #     # return variants
    
    # # def dehydrate_reviews(self, item):
    # #     reviews = ItemReview.objects.all().filter(item=item)
    # #     return reviews.values_list('code', flat=True)
    # #     # return reviews

    # # # def dehydrate_options(self, item):
    # # #     options = ItemOption.objects.all().filter(item=item)
    # # #     return options#.values_list('code', flat=True)
    
