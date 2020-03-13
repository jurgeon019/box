from django.apps import AppConfig


class FaqConfig(AppConfig):
    name = 'box.faq'
    verbose_name = 'FAQ'
    verbose_name_plural = 'FAQs'


default_app_config = 'box.faq.FaqConfig'

