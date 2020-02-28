
from modeltranslation.translator import translator

from box.shop.novaposhta.models import Warehouse


translator.register(Warehouse, fields=['title', 'address'])
