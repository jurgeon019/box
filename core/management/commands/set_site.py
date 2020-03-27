from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):

  def add_arguments(self, parser):
    parser.add_argument(
      'site_name',
      type=str,
      help='Site name'
    )

  def handle(self, *args, **kwargs):
    site        = Site.objects.all().first()
    site.domain = kwargs['site_name']
    site.name   = kwargs['site_name']
    site.save()
    self.stdout.write(self.style.SUCCESS('Data imported successfully'))



