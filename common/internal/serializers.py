from rest_framework_gis.fields import GeometryField
from rest_framework import serializers
from django.contrib.gis.geos import GeometryCollection

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
        'VectorLayerContent': InternalLayerContentSerializer
    }

    def to_representation(self, instance):
        serializer_cls = self.serializers_map[instance.__class__.__name__]
        return serializer_cls(instance).data

class VectorPOSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        properties = {k: v for k, v in instance.properties.items()}
        properties["name"] = instance.name
        properties["datetime"] = instance.date
        properties["styles"] = serialize_styles(instance.styles)
        return {
            'type': 'Feature',
            'geometry': GeometryField().to_representation(GeometryCollection(instance.geometry)),
            'properties': properties,
        }
    
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
        res['layer_type'] = 'V'
        return res