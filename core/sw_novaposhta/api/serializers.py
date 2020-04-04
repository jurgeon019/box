from rest_framework.serializers import ModelSerializer 
from ..models import * 



class WarehouseSerializer(ModelSerializer):
    class Meta:
        model = Warehouse 
        exclude = []


class AreaSerializer(ModelSerializer):
    class Meta:
        model = Area 
        exclude = []


class RegionSerializer(ModelSerializer):
    area = AreaSerializer()
    class Meta:
        model = Region 
        exclude = []


class SettlementSerializer(ModelSerializer):
    region = RegionSerializer()
    class Meta:
        model = Settlement 
        exclude = []
