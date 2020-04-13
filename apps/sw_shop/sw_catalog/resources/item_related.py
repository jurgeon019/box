from import_export.resources import ModelResource
from ..models import ItemManufacturer

class ItemManufacturerResource(ModelResource):
    class Meta:
        model = ItemManufacturer
        exclude = []