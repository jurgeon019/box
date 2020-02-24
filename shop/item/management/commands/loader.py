from django.core.management.base import BaseCommand
from box.shop.item.utils.parser import Parser, ExportMixin, ImportMixin


class Command(BaseCommand):

  def add_arguments(self, parser):

    parser.add_argument(
      '-f',
      '--file_name',
      type=str, 
      help='Назва файлу'
    )

    parser.add_argument(
        '-c',
        '--content_type',
        type=str,
        help='Тип контенту(item, category, item_category)',
    )

    parser.add_argument(
        '-a',
        '--action_type',
        type=str,
        help="Тип дії(import, export)"
    )

  def handle(self, *args, **kwargs):
    '''
    python manage.py loader -a=export -f=file_name.xlsx -c=item
    python manage.py loader -a=export -f=file_name.xlsx -c=category
    python manage.py loader -a=export -f=file_name.xlsx -c=item_category

    python manage.py loader -a=import -f=file_name.xlsx -c=item
    python manage.py loader -a=import -f=file_name.xlsx -c=category
    python manage.py loader -a=import -f=file_name.xlsx -c=item_category
    '''
    exporter       = ExportMixin()
    importer       = ImportMixin()
    file_name      = kwargs.get('file_name', "items.xlsx")
    content_type   = kwargs.get('content_type', 'item_category')
    action_type    = kwargs.get('action_type', 'import')
    file_extension = filename.split('.')[-1]


    if file_extension == 'csv':
      if content_type == 'item_category':

        if action_type == 'import':
          status = False
        elif action_type == 'export':
          status = False

      elif content_type == 'item':

        if action_type == 'import':
          status = importer.read_items_from_csv(filename)
        elif action_type == 'export':
          status = exporter.write_items_to_csv(filename)

      elif content_type == 'category':

        if action_type == 'import':
          status = importer.read_categories_from_csv(filename)
        elif action_type == 'export':
          status = exporter.write_categories_from_csv



    if file_extension == 'xlsx':
      if content_type == 'item_category':

        if action_type == 'import':
          status = importer.read_items_categories_from_xlsx(filename)
        elif action_type == 'export':
          status = exporter.write_items_categories_to_xlsx(filename)

      elif content_type == 'item':

        if action_type == 'import':
          status = importer.read_items_from_xlsx(filename)
        elif action_type == 'export':
          status = exporter.write_items_to_xlsx(filename)

      elif content_type == 'category':

        if action_type == 'import':
          status = importer.read_categories_from_xlsx(filename)
        elif action_type == 'export':
          status = exporter.write_categories_to_xlsx(filename)



    if file_extension == 'json':
      if content_type == 'item_category':

        if action_type == 'import':
          status = False
        elif action_type == 'export':
          status = False

      elif content_type == 'item':

        if action_type == 'import':
          status = False 
        elif action_type == 'export':
          status = False

      elif content_type == 'category':

        if action_type == 'import':
          status = False 
        elif action_type == 'export':
          status = False



    if file_extension == 'xml':
      if content_type == 'item_category':

        if action_type == 'import':
          status = False
        elif action_type == 'export':
          status = exporter.export_items_to_xml(file_name=file_name, *args, **kwargs)


      elif content_type == 'item':

        if action_type == 'import':
          status = False 
        elif action_type == 'export':
          status = False

      elif content_type == 'category':

        if action_type == 'import':
          status = False 
        elif action_type == 'export':
          status = False



    if status:
      self.stdout.write(self.style.SUCCESS('Data imported successfully'))
    else:
      self.stdout.write(self.style.ERROR('Data import FAILED'))



