from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.http import require_GET
from ..module_config import COMMANDS
from rest_framework.generics import ListAPIView
from .base_serializers import AreaSerializer, LayerSerializer
from .base_models import Area, Layer
from rest_framework.decorators import api_view, renderer_classes

@api_view(('GET', ))
def get_commands(request):
    return Response(data={k: {'alias': v.alias, 'description': v.description} for k, v in COMMANDS.items()})

@api_view(('GET', ))
def run_command(request, command_name):
    if command_name not in COMMANDS:
        return Response(data=['No such command'], status=status.HTTP_404_NOT_FOUND)
    return COMMANDS[command_name].run(request)

class ListAreaView(ListAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

class ListLayerView(ListAPIView):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer