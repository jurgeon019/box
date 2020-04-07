from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProjectConfig(AppConfig):
    name = 'project'
    verbose_name = _("Проект")
    verbose_name_plural = verbose_name
