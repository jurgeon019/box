from django import apps
from django.utils.translation import gettext_lazy as _


class EditorConfig(apps.AppConfig):
    name = 'box.editor'
    verbose_name = _('Редактор')
    verbose_name_plural = verbose_name



default_app_config = 'box.editor.EditorConfig'



