from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView
from . import models, serializers
from .forms import GISModuleForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_gis.pagination import GeoJsonPagination
import importlib


class ModuleListView(ListAPIView):
    serializer_class = serializers.ModuleListSerializer
    queryset = models.GISModule.objects.all()

class AreaListView(ListAPIView):
    serializer_class = serializers.AreaListSerializer

    def get_queryset(self):
        return models.Area.objects.path_filter(self.kwargs)

class LayerListView(ListAPIView):
    serializer_class = serializers.LayerSerializer

    def get_queryset(self):
        return models.Layer.objects.path_filter(self.kwargs)


class LayerContentListView(ListAPIView):

    def get_queryset(self):
        layer = models.Layer.objects.path_get(self.kwargs)
        feature_cls = models.VectorFeature if layer.is_vector() else models.RasterFeature
        self.pagination_class = GeoJsonPagination if layer.is_vector() else None
        # TODO:
        self.serializer_class = serializers.VectorFeatureSerializer if layer.is_vector() else None

        features_filtered = feature_cls.objects.filter_features(self.kwargs["layer_name"],
                                                       self.kwargs["area_name"])
        
        datetime_start = self.request.query_params.get('datetime_start')
        if datetime_start is not None:
            features_filtered = feature_cls.objects.datetime_filter(features_filtered,
                                                                    datetime_start,
                                                                    self.request.query_params.get('datetime_end'))

        if layer.is_vector():
            # TODO: vector specific filters
            pass
        else:
            # TODO: raster specific filters
            pass

        return features_filtered


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
    gis_module = get_object_or_404(models.GISModule, name=module_name)
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