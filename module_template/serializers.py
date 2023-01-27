from rest_framework import serializers

class SomeCommandSerializer(serializers.Serializer):
    int_param = serializers.IntegerField()
    string_param =  serializers.CharField(max_length=2)

    def validate_int_param(self, val):
        if val not in range(0, 5):
            raise serializers.ValidationError("int param should be in range [0, 5)")
        return val

    def validate_string_param(self, val):
        if "test" not in val:
            raise serializers.ValidationError("string_param should contain 'test' word")
        return val



    