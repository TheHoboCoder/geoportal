from rest_framework import serializers
from common import serializers as geo_serializers

class DrawLineSerializer(serializers.Serializer):
    int_param = serializers.IntegerField(label="Количество", min_value=1, max_value=5)
    string_param = serializers.CharField(label="Введите test", max_length=50)
    point_start = geo_serializers.PointField()
    point_end = geo_serializers.PointField()

    def validate_string_param(self, val):
        if "test" not in val:
            raise serializers.ValidationError("string_param should contain 'test' word")
        return val




    