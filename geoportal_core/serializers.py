from rest_framework import serializers
from .models import GISModule, Area, Layer

class ModuleListSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GISModule
        fields = '__all__'

class AreaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['name', 'alias', 'point_min', 'point_max']

class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer
        fields = ['name', 'alias', 'ordering', 'layer_type']