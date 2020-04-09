from django.apps import AppConfig

class CustomAdminConfig(AppConfig):
    label = 'sw_admin'
    name = 'box.apps.sw_admin'
    verbose_name = ("Адмін")
