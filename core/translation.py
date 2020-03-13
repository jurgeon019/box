
from modeltranslation.translator import translator 
from django.apps import apps

models = apps.get_models()

for klass in models:
    fields = getattr(klass, 'modeltranslation_fields', None)
    if fields:
        translator.register(klass, fields=fields())




