from django.core.management.base import BaseCommand

from box.shop.item.utils import read_items_from_xlsx, export_items_to_xml

class Command(BaseCommand):
  
  def handle(self, *args, **kwargs):
    status = export_items_to_xml()
    if status:
      self.stdout.write(self.style.SUCCESS('Data imported successfully'))
    else:
      self.stdout.write(self.style.ERROR('Data import FAILED'))

