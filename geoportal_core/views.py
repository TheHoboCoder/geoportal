from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from . import models, serializers
from .forms import CreateGISModuleForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_gis.pagination import GeoJsonPagination
from common.internal.modules import MODULES

def show_map(request, module_name):
    return render(request, 'map.html', { 
        'module': models.GISModule.objects.get(name=module_name),
    })

def module_list(request):
    return render(request, 'module_list.html', 
                  {'module_list': models.GISModule.objects.all()})

class ModuleListView(ListAPIView):
    serializer_class = serializers.ModuleListSerializer
    queryset = models.GISModule.objects.all()

class AreaListView(ListAPIView):
    serializer_class = serializers.AreaListSerializer

    def get_queryset(self):
        return models.Area.objects.path_filter(self.kwargs)
    
class AreaDetailView(RetrieveAPIView):
    serializer_class = serializers.AreaListSerializer
    lookup_field = "name"
    lookup_url_kwarg = "area_name"

    def get_queryset(self):
        return models.Area.objects.filter(module__name=self.kwargs["module_name"])

class LayerListView(ListAPIView):
    serializer_class = serializers.LayerSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['kwargs'] = self.kwargs
        return context

    def get_queryset(self):
        return models.Layer.objects.path_filter(self.kwargs)


class LayerContentListView(ListAPIView):

    def get_queryset(self):
        layer = models.Layer.objects.path_get(self.kwargs)
        feature_cls = models.VectorFeature if layer.is_vector() else models.RasterFeature
        self.pagination_class = GeoJsonPagination if layer.is_vector() else None
        self.serializer_class = serializers.VectorFeatureSerializer if layer.is_vector() else serializers.RasterFeatureSerializer

        features_filtered = feature_cls.objects.filter_features(
                                                       self.kwargs["module_name"],
                                                       self.kwargs["layer_name"],
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

def get_module_config(module_name):
    gis_module = get_object_or_404(models.GISModule, name=module_name)
    return MODULES[module_name]

@api_view(('GET', ))
def get_commands(request, module_name):
    module_config = get_module_config(module_name)
    return Response(data=module_config.command_list.description)

@api_view(('GET', ))
def run_command(request, module_name, command_name):
    module_config = get_module_config(module_name)
    if command_name not in module_config.command_list.commands:
        return Response(data=['No such command'], status=status.HTTP_404_NOT_FOUND)
    return module_config.command_list.commands[command_name].run(request)