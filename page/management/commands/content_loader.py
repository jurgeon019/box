from django.core.management.base import BaseCommand 

from box.imp_exp.main import Content


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-f',
            '--filename',
        )
        parser.add_argument(
            '-a',
            '--action_type'
        )
    def handle(self, *args, **kwargs):
        content     = Content()
        filename    = kwargs['filename']
        action_type = kwargs['action_type'] 
        if action_type == 'import':
            content.import_content(filename)
        elif action_type == 'export':
            content.export_content(filename)
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))








'''

read 
load 
import 


write
unload
export


'''