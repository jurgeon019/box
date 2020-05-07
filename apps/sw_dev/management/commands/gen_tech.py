from django.core.management.base import BaseCommand
from box.apps.sw_shop.sw_catalog.models import Item, ItemCategory, Currency
from random import choice 


class Command(BaseCommand):
  def handle(self, *args, **kwargs):

    spec_rent_category = ItemCategory.objects.get(code="spec_rent")
    spec_sell_category = ItemCategory.objects.get(code="spec_sell")

    for i in range(1, 10):
        category = choice(spec_rent_category.subcategories.all())
        price    = choice([12000, 120000, 60000, 23000, 88500, 874000])
        currency = choice(Currency.objects.all())
        Item.objects.get_or_create(
            title=f'Техніка на оренду ({category.title}) ({i})',
            price=price,
            currency=currency,
            category=category,
        )
        category = choice(spec_sell_category.subcategories.all())
        currency = choice(Currency.objects.all())
        sell_item = Item.objects.get_or_create(
            title=f'Техніка на продажу ({category.title}) ({i})',
            price=price,
            currency=currency,
            category=category,
        )
    self.stdout.write(self.style.SUCCESS('Data imported successfully'))

