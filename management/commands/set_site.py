from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    site = Site.objects.all().first()
    site.domain = 'mottoex.com.ua'
    site.name   = 'mottoex.com.ua'
    site.save()
    self.stdout.write(self.style.SUCCESS('Data imported successfully'))

