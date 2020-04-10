from django.core.management.base import BaseCommand
from box.apps.sw_shop.sw_catalog.models import Item, ItemCategory, ItemImage



class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    parts    = ItemCategory.objects.get(code="parts")

    jcb_cat, _ = ItemCategory.objects.get_or_create(title__iexact='запчасти для jcb')
    jcb_cat.code = 'parts_jcb'
    jcb_cat.parent = parts 
    jcb_cat.save()

    # perkins_cat, _ = ItemCategory.objects.get_or_create(title__iexact='запчасти perkins')
    perkins_cat = ItemCategory.objects.get(title__iexact='запчастини perkins')
    perkins_cat.code = 'parts_perkins'
    perkins_cat.parent = parts 
    perkins_cat.save()

    # manitou_cat, _ = ItemCategory.objects.get_or_create(title__iexact='запчастини manitou')
    manitou_cat = ItemCategory.objects.get(title__iexact='запчастини manitou')
    manitou_cat.code = 'parts_manitou'
    manitou_cat.parent = parts 
    manitou_cat.save()

    # spec_rent_category = ItemCategory.objects.get(code="spec_rent")
    # spec_sell_category = ItemCategory.objects.get(code="spec_sell")

    manitou, _ = Item.objects.get_or_create(
      title = 'Manitou',
      category = manitou_cat, 
    )
    ItemImage.objects.create(
      item = manitou,
      image = 'dev/manitou.jpg'
    )
    manitou.create_thumbnail_from_images()


    self.stdout.write(self.style.SUCCESS('Data imported successfully'))

