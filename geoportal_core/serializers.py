from rest_framework import serializers
from .models import GISModule, Area, Layer, VectorFeature, RasterFeature
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.urls import reverse, resolve
from common.models import URLLayerContent
from common.internal.serializers import URLLayerContentSerializer, serialize_styles
from common.internal.modules import MODULES

class ModuleListSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GISModule
        fields = '__all__'

class AreaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['name', 'alias', 'bbox']

class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer
        fields = ['name', 'alias', 'ordering', 'layer_type']

    def to_representation(self, instance):
        req = self.context["request"]
        path_kwargs = self.context["kwargs"]
        module_name = path_kwargs["module_name"]
        path_kwargs["layer_name"] = instance.name
        res = super().to_representation(instance)
        path = req.build_absolute_uri(reverse("layer_content", kwargs=path_kwargs))
        if instance.is_vector():
            res["layer_content"] = URLLayerContentSerializer(URLLayerContent(path)).data
            res["styles"] = serialize_styles(MODULES[module_name].layer_styles[instance.name])
        else:
           res["layer_content"] = {"type": "url", "url": path} 
        return res

class VectorFeatureSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = VectorFeature
        fields = ['name', 'properties', 'geometry', 'datetime']
        geo_field = 'geometry'
        auto_bbox = True

    def get_properties(self, instance, fields):
        p = instance.properties
        p["datetime"] = instance.datetime
        p["name"] = instance.name
        p["styles"] = []
        module_info = MODULES[instance.layer.module.name]
        layer_name = instance.layer.name 
        if layer_name in module_info.layer_style_functions:
            styles = module_info.layer_style_functions[layer_name](instance.to_po())
            p["styles"] = serialize_styles(styles)
        return p
    

class RasterFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = RasterFeature
        fields = ['name', 'datetime', 'raster_file']

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res["extent"] = instance.extent.extent
        return res