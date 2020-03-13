from django.apps import AppConfig


class PageConfig(AppConfig):
    name = 'box.page'
    verbose_name = 'Сторінки'
    def ready(self):
        from django.urls import path 
        from django.conf import settings 
        # from box.page.urls import urlpatterns
        # from box.page.views import pages_generator
        # urls_in_db = settings.CMS_TEMPLATES
        # for url_in_db in urls_in_db:
        #     urlpatterns.append(path(url_in_db,
        #                             pages_generator,
        #                             {'param':url_in_db},
        #                             name=url_in_db)
        #     )



