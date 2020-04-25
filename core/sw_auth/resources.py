from import_export.resources import ModelResource
from import_export.fields import Field
from .models import *
from box.core.utils import get_multilingual_fields 

from django.contrib.auth import get_user_model 



class BoxUserResource(ModelResource):
    # orders = Field()#TODO: orders  
    class Meta:
        model = get_user_model() 
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