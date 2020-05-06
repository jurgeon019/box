from rest_framework.serializers import ModelSerializer
from .models import * 


class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currency 
        exclude = []