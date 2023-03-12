from django.shortcuts import render
from common.commands import CommandResponse, CommandView
from .serializers import DrawLineSerializer
from common.models import VectorFeaturePO
from django.contrib.gis.geos import LineString

class DrawLineView(CommandView):
    serializer_class = DrawLineSerializer
    name="draw_line_command"
    description = "Рисует линию между двумя точками"
    alias = "Пример команды 1"

    def handler(self, validated_data):
        return CommandResponse([], [
            VectorFeaturePO({"line": validated_data['int_param']}, 
                            (LineString(validated_data['point_start'], validated_data['point_end'])))
        ], {
            'msg': f"{validated_data['string_param']} has some {validated_data['int_param']} in it. Awesome"
        })



