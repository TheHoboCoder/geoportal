from django.shortcuts import render
from .base.base_views import CommandView
from serializers import SomeCommandSerializer

class ExampleView(CommandView):
    serializer_class = SomeCommandSerializer

    def handle(self, validated_data):
        return {
            'msg': f"{validated_data['string_param']} has some {validated_data['int_param']}"
        }



