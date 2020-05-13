import csv
from django.core.management.base import BaseCommand
from datetime import datetime 
from pathlib import Path
from datetime import datetime 
from io import StringIO, BytesIO
from tablib import Dataset
from box.core.utils import get_resource, get_resources



class CommandMixin(object):

  def loader(self, extention, file_name, resource_name, time, *args, **kwargs):
    Resource       = get_resource(resource_name)
    dataset = Dataset()

    with open(file_name, 'r') as f:
      # imported_data = dataset.load(f.read())
      dataset.load(f.read(), format=file_name.split('.')[-1])
    result = Resource().import_data(dataset, dry_run=True)
    if not result.has_errors():
      Resource().import_data(dataset, dry_run=False)  
      return True 
    else:
      for error in result.row_errors():
        row = error[0]
        error = error[1][0]
        print(error.traceback)
        print(f"ERROR IN {row} LINE IN FILE {file_name}:", error.error)
        raise Exception(error.error)
      return False 

  def make_backup(self, *args, **kwargs):
    resources = get_resources()
    time      = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    for resource in resources:
      # print(resource)
      folder_name = f'backups/{time}/' # + resource.model.appname
      file_name = f'{resource.__name__}.csv'
      path_name = folder_name + file_name
      Path(folder_name).mkdir(parents=True, exist_ok=True)
      with open(path_name, 'w') as f:
        f.write(getattr(resource().export(), 'csv'))
    return True 

  def load_from_init(self, *args, **kwargs):
      items = [dct for dct in map(dict, csv.DictReader(open(init_filename)))] 
      for item in items:
          load           = item['load']
          file_name      = item['file_name']
          extention      = item['extention']
          resource_name  = item['resource_name']
          if bool(int(load)):
              result = loader(extention, file_name, resource_name, time)
              return result 

  def load_from_file(self, *args, **kwargs):
      time = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
      file_name      = kwargs['file_name']
      extention      = kwargs.get('extention')
      resource_name  = kwargs.get('resource_name')
      if not extention:
          extention = 'csv'
      if not resource_name:
          resource_name = f"{file_name.split('/')[-1].split('.')[0]}Resource"
      result = loader(extention, file_name, resource_name, time)
      return result 
  

class Command(BaseCommand, CommandMixin):
  def add_arguments(self, parser):
      parser.add_argument(
          '-f',
          '--file_name',
      )
      parser.add_argument(
          '-e',
          '--extention',
      )
      parser.add_argument(
          '-r',
          '--resource_name',
      )
      parser.add_argument(
          '-i',
          '--init_filename',
      )
      parser.add_argument(
          '-b',
          '--backup',
      )

  def handle(self, *args, **kwargs):
      result = None 
      init_filename = kwargs.get('init_filename')
      backup        = kwargs.get('backup')
      print(args)
      print(kwargs)

      if backup:
        print(backup)
        result = self.make_backup(*args, **kwargs)
        self.print_message(result)
        return 

      # if init_filename:
      #   result = self.load_from_init(*args, **kwargs)
      #   self.print_message(result)
  
      # elif not init_filename:
      #   result = self.load_from_file(*args, **kwargs)
      #   self.print_message(result)

  def print_message(self, result):
    if result:
      self.stdout.write(self.style.SUCCESS('Data imported successfully'))
    else:
      self.stdout.write(self.style.ERROR('DATA HAVENT IMPORTED'))



