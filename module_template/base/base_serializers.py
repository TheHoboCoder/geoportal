from .base_models import Area, Layer
from rest_framework import serializers

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area

class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer