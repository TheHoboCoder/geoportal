from rest_framework_gis.fields import GeometryField
from rest_framework import serializers
from django.contrib.gis.geos import GeometryCollection
import base64
from pathlib import Path

class VectorStyleSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return instance.to_representation()
    
def serialize_styles(styles):
    return VectorStyleSerializer(styles, many=True).data
    
class InternalLayerContentSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'type': 'internal',
            'geojson': GeoJsonSerializer(instance.vector_objects).data
        }
    
class InternalRasterContentSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'type': 'internal',
            'rasters': RasterPOSerializer(instance.raster_objects, many=True).data
        }

class URLLayerContentSerializer(serializers.Serializer):
    url = serializers.URLField()
    srid = serializers.IntegerField()

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['type'] = 'url'
        res['format'] = instance.format.value
        return res

class LayerContentSerializer(serializers.Serializer):
    serializers_map = {
        'URLLayerContent': URLLayerContentSerializer,
        'VectorLayerContent': InternalLayerContentSerializer,
        'RasterLayerContent': InternalRasterContentSerializer
    }

    def to_representation(self, instance):
        serializer_cls = self.serializers_map[instance.__class__.__name__]
        return serializer_cls(instance).data
    
class FeatureSerializer(serializers.Serializer):
    name = serializers.CharField()
    date = serializers.DateTimeField()

class VectorPOSerializer(FeatureSerializer):
    def to_representation(self, instance):
        res = super().to_representation(instance)
        properties = {k: v for k, v in instance.properties.items()}
        properties["styles"] = serialize_styles(instance.styles)
        res["type"] = "Feature"
        res["geometry"] = GeometryField().to_representation(GeometryCollection(instance.geometry))
        res["properties"] = properties
        return res
    
class RasterPOSerializer(FeatureSerializer):
    extent = serializers.ListField()

    def to_representation(self, instance):
        res = super().to_representation(instance)
        # if instance.file.size > 150 * 1024:
        #     raise Exception("too large image file")
        #extension = Path(instance.file.path).suffix.strip('.')
        encoded_string = base64.b64encode(instance.file.read())
        # with instance.file.open('rb') as img_f:
            
        res["raster_file"] = f'data:image/png;base64,{encoded_string.decode("utf-8")}'
        return res

class GeoJsonSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'type': 'FeatureCollection',
            'features': VectorPOSerializer(instance, many=True).data
        }

class LayerPOSerializer(serializers.Serializer):
    name = serializers.SlugField()
    alias = serializers.CharField()
    ordering = serializers.IntegerField()
    styles = VectorStyleSerializer(many=True)
    layer_content = LayerContentSerializer()

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['layer_type'] = 'V' if instance.is_vector else 'R'
        return res