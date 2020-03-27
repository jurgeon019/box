from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class PageConfig(AppConfig):
    name = 'box.content'
    verbose_name = _('Контент')
    def ready(self):
        from django.urls import path 
        from django.conf import settings 
        # from box.content.urls import urlpatterns
        # from box.content.views import pages_generator
        # urls_in_db = settings.CMS_TEMPLATES
        # for url_in_db in urls_in_db:
        #     urlpatterns.append(path(url_in_db,
        #                             pages_generator,
        #                             {'param':url_in_db},
        #                             name=url_in_db)
        #     )





default_app_config = 'box.content.PageConfig'