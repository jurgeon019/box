from import_export.resources import ModelResource
from import_export.fields import Field 
from ..models.attribute import * 


class AttributeResource(ModelResource):
    class Meta:
        model = Attribute
        exclude =  []
    def before_import_row(self, row, **kwargs):
        if row.get('code') == '':
            row['code'] = None 



class AttributeCategoryResource(ModelResource):
    class Meta:
        model = AttributeCategory
        exclude =  []


class ItemAttributeValueResource(ModelResource):
    class Meta:
        model = ItemAttributeValue
        exclude =  []


class AttributeValueResource(ModelResource):
    class Meta:
        model = AttributeValue
        exclude =  []
        # import_id_fields = [
        #     'id',
        #     'code',
        #     'value',
        # ]
    def before_import_row(self, row, **kwargs):
        if row.get('code') == '':
            row['code'] = None 


class ItemAttributeResource(ModelResource):
    class Meta:
        model = ItemAttribute
        exclude = []
    # value_names = Field(
    #     attribute=None, 
    #     column_name='value_names',
    # )
    # def get_import_id_fields(self):
    #     return [
    #         'id',
    #     ]
    # def get_export_order(self):
    #     return [
    #         'id',
    #         'is_option',
    #         'attribute',
    #         'value_names',
    #     ]
    # def before_import_row(self, row, **kwargs):
    #     if row.get('value_names'):
    #         value_names = row['value_names']
    #         value_names = value_names.split(';;\n')
    #         for value in value_names:
    #             value = value.strip().lower()
    #             v = ItemAttributeValue.objects.get_or_create(
    #                 value__value=value,
    #                 item_attribute=row['id'],
    #             )[0]
    #     if row.get('attribute'):
    #         attribute = row['attribute'].lower().strip()
    #         attribute = Attribute.objects.get_or_create(name=attribute)[0]
    #         attribute = attribute.name
    #         row['attribute'] = attribute




