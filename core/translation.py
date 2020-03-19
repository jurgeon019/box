
from modeltranslation.translator import translator 
from django.apps import apps


for klass in apps.get_models():
    if hasattr(klass, 'modeltranslation_fields'):
        translator.register(klass, fields=klass.modeltranslation_fields())




