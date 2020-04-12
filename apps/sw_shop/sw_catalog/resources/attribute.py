from import_export.resources import ModelResource
from ..models.attribute import * 



class AttributeResource(ModelResource):
    class Meta:
        model = Attribute
        exclude =  []
