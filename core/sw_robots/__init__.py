from pkg_resources import get_distribution

__version__ = get_distribution("django-robots").version

from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _

class RobotsConfig(AppConfig):
    verbose_name = _("Robots")
    verbose_name_plural = verbose_name
    name = 'box.core.sw_robots'