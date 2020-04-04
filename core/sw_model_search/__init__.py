
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


from box.core.sw_model_search.lib import (
    normalize_query, model_search, tags_search, build_query)


__all__ = ['normalize_query', 'build_query', 'model_search']


class ModelSearchConfig(AppConfig):
    name = 'box.core.sw_model_search'
    verbose_name = _("Search")


default_app_config = 'box.core.sw_model_search.ModelSearchConfig'
