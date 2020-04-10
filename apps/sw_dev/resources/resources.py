
from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget
from import_export.fields import Field
from ..models import *
# Category, Item 
from mptt import models 
    # https://github.com/django-import-export/django-import-export/issues/577
    # https://stackoverflow.com/questions/25670553/adding-foreignkey-widget-to-django-import-export
    # https://django-import-export.readthedocs.io/en/latest/api_widgets.html#import_export.widgets.ForeignKeyWidget


class CategoryResource(ModelResource):

    parent = Field(
        column_name='parent',
        attribute='parent',
        widget=ForeignKeyWidget(Category, field='id')
    )
    class Meta:
        model = Category
        exclude = [
            'lft',
            'rght',
            'tree_id',
            'level',
        ]
    def get_export_order(self):
        return [
            'id',
            'parent',
            'title',
            'code',
        ]
    def before_import_row(self, row, **kwargs):
        print()
        print(row)
        print('**')
        if row['code'] == '':
            row['code'] = None
        print(row)
        print()


class ItemResource(ModelResource):
    class Meta:
        model = Item
        exclude = [
            
        ]

