from import_export.resources import ModelResource
from import_export.fields import Field
from .models import *
from box.core.utils import get_multilingual_fields 


class BoxUserResource(ModelResource):
    # orders = Field()#TODO: orders  
    class Meta:
        model = BoxUser 
        exclude = [
            "group",            # TODO: customer_group 
            "groups",           # TODO: groups 
            "user_permissions", # TODO: permissions 
            "last_login",
            "date_joined",
        ]

    def get_export_order(self):
        export_order = [
            "id",	
            "is_superuser",
            "is_staff",
            "is_active",
            "first_name",
            "username",
            "last_name",
            "email",
            "phone_number",
            "address",
            "birth_date",
            "gender",
            "password",
        ]
        return export_order

    def get_import_id_fields(self):
        import_id_fields = [
            'id',
        ]
        return import_id_fields

    # def dehydrate_page(self, obj):
    #     page = None 
    #     if obj.page:
    #         page = obj.page.code 
    #     return page 

    # def before_import_row(self, row, **kwargs):
    #     if row['page']:
    #         row['page'] = Page.objects.get_or_create(code=row['page'])[0].id
