from rest_framework import serializers
from .models import GISModule

class ModuleListSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GISModule
        fields = '__all__'