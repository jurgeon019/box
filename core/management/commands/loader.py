from django.core.management.base import BaseCommand
from box.core.utils import loader 
import csv
from datetime import datetime 


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
            '--init_filename',
        )
    def handle(self, *args, **kwargs):
        init_filename = kwargs.get('init_filename')
        time = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
        if init_filename:
            items = [dct for dct in map(dict, csv.DictReader(open(init_filename)))] 
            for item in items:
                # print("\n item:\n", item)
                # print("\n kwargs:\n", kwargs)
                load           = item['load']
                file_name      = item['file_name']
                extention      = item['extention']
                action_type    = item['action_type']
                resource_name  = item['resource_name']
                print(resource_name)
                if bool(int(load)):
                    result = loader(extention, file_name, action_type, resource_name, time)
                    if result:
                        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
                    else:
                        self.stdout.write(self.style.ERROR('DATA HAVENT IMPORTED'))
        elif not init_filename:
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
            result = loader(extention, file_name, action_type, resource_name, time)
            if result:
                self.stdout.write(self.style.SUCCESS('Data imported successfully'))
            else:
                self.stdout.write(self.style.ERROR('DATA HAVENT IMPORTED'))




