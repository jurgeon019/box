from django.core.management.base import BaseCommand
from box.core.utils import loader 



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
    def handle(self, *args, **kwargs):
        '''
        python manage.py loader -f=babaski.csv -e=csv -r=ContentResource -a=import
        python manage.py loader -f=babaski.csv -e=csv -r=ItemResource -a=export
        python manage.py loader -f=babaski.xlsx -e=xlsx -r=ContentResource -a=import
        python manage.py loader -f=babaski.xlsx -e=xlsx -r=ContentResource -a=export
        '''
        extention      = kwargs['extention']
        file_name      = kwargs['file_name']
        action_type    = kwargs['action_type']
        resource_name  = kwargs['resource_name']
        result = loader(extention, file_name, action_type, resource_name)
        if result:
            self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        else:
            self.stdout.write(self.style.ERROR('DATA HAVENT IMPORTED'))




