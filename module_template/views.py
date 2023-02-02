from django.shortcuts import render
from common.commands import CommandResponse, CommandView
from .serializers import SomeCommandSerializer

class ExampleView(CommandView):
    serializer_class = SomeCommandSerializer
    name="some_command"
    description = "Пример команды"
    alias = "Просто команда"

    def handler(self, validated_data):
        return CommandResponse([], {}, {
            'msg': f"{validated_data['string_param']} has some {validated_data['int_param']}"
        })



