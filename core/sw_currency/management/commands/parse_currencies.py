from django.core.management.base import BaseCommand
from ...views import parse_currencies

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        parse_currencies()
        print('ok')
