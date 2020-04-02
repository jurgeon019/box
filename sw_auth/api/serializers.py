from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model 
from django.contrib.auth.models import Group, Permission 







class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        exclude = [
        ]



class PermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        exclude = [
        ]



class UserSerializer(ModelSerializer):
    # TODO: permissions
    # TODO: group
    class Meta:
        model = get_user_model()
        exclude = [
            'password',
        ]


