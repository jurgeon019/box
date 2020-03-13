from django import apps 


class ContactFormConfig(apps.AppConfig):
    name = 'box.contact_form'
    verbose_name = 'Контактні форми'

default_app_config = 'box.contact_form.ContactFormConfig'


