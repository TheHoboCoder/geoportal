from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView
from .serializers import ModuleListSerializer, AreaListSerializer, LayerSerializer
from .models import GISModule, Area, Layer
from .forms import GISModuleForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import importlib
from django.db.models import Q

class ModuleListView(ListAPIView):
    serializer_class = ModuleListSerializer
    queryset = GISModule.objects.all()

class AreaListView(ListAPIView):
    serializer_class = AreaListSerializer

    def get_queryset(self):
        return Area.objects.filter(module__name=self.kwargs["module_name"])

class LayerListView(ListAPIView):
    serializer_class = LayerSerializer

    def get_queryset(self):
        return Layer.objects.filter(Q(module__name=self.kwargs["module_name"]) & 
                                   (Q(area__name__isnull=True) | 
                                    Q(area__name=self.kwargs["area_name"])) )


def create_module(request):
    # TODO: redirect to login
    if not request.user.is_authenticated:
        return HttpResponse('must authorize', status=403)
    if request.method == 'POST':
        form = GISModuleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(owner=request.user)
            return HttpResponseRedirect('create_succes/')

    else:
        form = GISModuleForm()

    return render(request, 'geoportal_core/add_module.html', {'form': form})

def on_created(request):
    return HttpResponse('<b>Uploaded</b>')

def get_module_config(module_name):
    gis_module = get_object_or_404(GISModule, name=module_name)
    return importlib.import_module(f"{module_name}.module_config", package=None)

@api_view(('GET', ))
def get_commands(request, module_name):
    module_config = get_module_config(module_name)
    return Response(data=module_config.COMMANDS.description)

@api_view(('GET', ))
def run_command(request, module_name, command_name):
    module_config = get_module_config(module_name)
    if command_name not in module_config.COMMANDS.commands:
        return Response(data=['No such command'], status=status.HTTP_404_NOT_FOUND)
    return module_config.COMMANDS.commands[command_name].run(request)