from django.core.management.base import BaseCommand
from box.core.utils import loader 
import csv


class Command(BaseCommand):
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
            '-a',
            '--action_type',
        )
        parser.add_argument(
            '-i',
            '--initial_import_commands_filename',
        )
    def handle(self, *args, **kwargs):
        '''
        python manage.py loader -f=babaski.csv -e=csv -r=ContentResource -a=import
        python manage.py loader -f=babaski.csv -e=csv -r=ItemResource -a=export
        python manage.py loader -f=babaski.xlsx -e=xlsx -r=ContentResource -a=import
        python manage.py loader -f=babaski.xlsx -e=xlsx -r=ContentResource -a=export
        '''
        initial_import_commands_filename = kwargs.get('initial_import_commands_filename')
        if initial_import_commands_filename:
            items = [dct for dct in map(dict, csv.DictReader(open(initial_import_commands_filename)))] 
            for item in items:
                print("item:")
                print(item)
                load           = item['load']
                file_name      = kwargs['file_name']
                extention      = kwargs['extention']
                action_type    = kwargs['action_type']
                resource_name  = kwargs['resource_name']
                if bool(int(load)):
                    result = loader(extention, file_name, action_type, resource_name)
                    if result:
                        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
                    else:
                        self.stdout.write(self.style.ERROR('DATA HAVENT IMPORTED'))
        elif not initial_import_commands_filename:
            file_name      = kwargs['file_name']
            extention      = kwargs.get('extention')
            action_type    = kwargs.get('action_type')
            resource_name  = kwargs.get('resource_name')
            if not extention:
                extention = 'csv'
            if not action_type:
                action_type = 'import'
            if not resource_name:
                resource_name = f"{file_name.split('/')[-1].split('.')[0]}Resource"
            result = loader(extention, file_name, action_type, resource_name)
            if result:
                self.stdout.write(self.style.SUCCESS('Data imported successfully'))
            else:
                self.stdout.write(self.style.ERROR('DATA HAVENT IMPORTED'))




