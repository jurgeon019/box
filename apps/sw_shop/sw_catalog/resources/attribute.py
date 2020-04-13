from import_export.resources import ModelResource
from import_export.fields import Field 
from ..models.attribute import * 


class AttributeResource(ModelResource):
    class Meta:
        model = Attribute
        exclude =  []


class AttributeCategoryResource(ModelResource):
    class Meta:
        model = AttributeCategory
        exclude =  []


class ItemAttributeVariantResource(ModelResource):
    class Meta:
        model = ItemAttributeVariant
        exclude =  []


class AttributeVariantValueResource(ModelResource):
    class Meta:
        model = AttributeVariantValue
        exclude =  []
        import_id_fields = [
            'id',
            'value',
        ]


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
    #             v = ItemAttributeVariant.objects.get_or_create(
    #                 value__value=value,
    #                 item_attribute=row['id'],
    #             )[0]
    #     if row.get('attribute'):
    #         attribute = row['attribute'].lower().strip()
    #         attribute = Attribute.objects.get_or_create(name=attribute)[0]
    #         attribute = attribute.name
    #         row['attribute'] = attribute




