from django.core.management.base import BaseCommand

from box.shop.item.utils import read_items_from_xlsx


class Command(BaseCommand):

  def add_arguments(self, parser):
    parser.add_argument(
      'file_name', 
      type=str, 
      help='File, that contains the main item\'s information'
    )

  def handle(self, *args, **kwargs):
    filename = kwargs['file_name']
    status   = read_items_from_xlsx(filename)
    if status:
      self.stdout.write(self.style.SUCCESS('Data imported successfully'))
    else:
      self.stdout.write(self.style.ERROR('Data import FAILED'))

