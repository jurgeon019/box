from django.core.management.base import BaseCommand
from ...views import handle_np


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-l',
            '--limit',
        )
        parser.add_argument(
            '-p',
            '--page',
        )
        parser.add_argument(
            '-pl',
            '--pages_limit',
        )
        parser.add_argument(
            '-a',
            '--action',
        )
        parser.add_argument(
            '-c',
            '--content',
        )
        parser.add_argument(
            '-t',
            '--type',
        )

        '''
        python3 manage.py np settlements -a=gen_json 
        python3 manage.py np settlements -a=gen_json -l=150 -p=1 -pl=5
        python3 manage.py np settlements -a=from_json 

        action  = refresh, browse
        content = warehouses, settlements 
        type    = gen_json, from_api, from_json 
        '''

    def handle(self, *args, **kwargs):
        limit       = kwargs.get('limit', 150)
        page        = kwargs.get('page', 1)
        pages_limit = kwargs.get('pages_limit', None)
        action      = kwargs.get('action','refresh')
        content     = kwargs.get('content','warehouses')
        type        = kwargs.get('type','from_json')
        query = {
            "limit":limit,
            "page":page,
            "pages_limit":pages_limit,
        }
        handle_np(query, action, content, type)
        self.stdout.write(self.style.SUCCESS('Success'))

