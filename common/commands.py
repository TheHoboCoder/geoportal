from rest_framework.response import Response
from geoportal_core.models import VectorFeature
from geoportal_core.serializers import VectorFeatureSerializer
from .internal.serializers import LayerPOSerializer
from drf_jsonschema_serializer import to_jsonschema

class CommandResponse:
    """gis_data - список объектов LayerPO с векторными объектами (см. models.py)
       custom_data - словарь с данными (только примитивные типы Python)
    """
    def __init__(self, layers, custom_data: dict):
        self.gis_data = layers
        self.custom_data = custom_data

    def serialize(self):
        return {
            'layers': LayerPOSerializer(self.gis_data, many=True).data,
            'custom_data': self.custom_data,
        }

class CommandView:
    # must set in subclass
    serializer_class = None
    description = ""
    alias = ""
    name = ""

    #TODO:
    def __init__(self):
        self.serializer_instance = self.serializer_class()
    
    def handler(self, validated_data) -> CommandResponse:
        pass

    def describe(self):
        return {'name': self.name,
                'alias': self.alias, 
                'description': self.description, 
                'schema': to_jsonschema(self.serializer_instance)}

    def run(self, request):
        serializer = self.serializer_class(data=request.GET)
        if serializer.is_valid(raise_exception=True):
            return Response(data=self.handler(serializer.validated_data).serialize())


class CommandList:
    def __init__(self, commands):
        self.commands = {command.name: command for command in commands}
        self.description = {command.name: command.describe() for command in commands}