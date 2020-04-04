from rest_framework import serializers 
from django.contrib.auth import get_user_model 
from django.contrib.auth.models import Group, Permission 







class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = [
        ]



class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        exclude = [
        ]



class UserSerializer(serializers.ModelSerializer):
    # TODO: permissions
    # TODO: group
    is_authenticated = serializers.SerializerMethodField()

    def get_is_authenticated(self, obj):
        return obj.is_authenticated 
    

    class Meta:
        model = get_user_model()
        exclude = [
            'password',
            'date_joined',
            'last_login',
        ]


