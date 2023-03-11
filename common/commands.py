from rest_framework.response import Response

class CommandResponse:
    """updated_layers - список названий слоев, которые были изменены в результате выполнения команды
       gis_data - новые слои и геоданные, формат в разработке 
       custom_data - словарь с данными (только примитивные типы Python)
    """
    def __init__(self, updated_layers, gis_data, custom_data: dict):
        self.updated_layers = updated_layers
        self.gis_data = gis_data
        self.custom_data = custom_data

    def serialize(self):
        return {'updated_layers': self.updated_layers, 
                'gis_data': self.gis_data,
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
        return {'alias': self.alias, 'description': self.description}

    def run(self, request):
        serializer = self.serializer_class(data=request.GET)
        if serializer.is_valid(raise_exception=True):
            response = self.handler(serializer.validated_data)
            return Response(data=response.serialize())


class CommandList:
    def __init__(self, commands):
        self.commands = {command.name: command for command in commands}
        self.description = {command.name: command.describe() for command in commands}