from rest_framework import serializers
from geoportal_core.models import VectorFeature
from django.db.models import Q

class WithinArea:
    requires_context = True

    def __call__(self, value, serializer):
        if not value.within(serializer.context['bbox']):
            raise serializers.ValidationError("Геометрия должна находиться внутри области")
        return value
    
class NoIntersections:
    requires_context = True

    def __init__(self, layer_name=None):
        self.layer_name = layer_name
    
    def __call__(self, value, serializer):
        query = Q(geometry__intersects=value) & Q(layer__module=serializer.context["module"])
        if self.layer_name is not None:
            query &= Q(layer__name=self.layer_name)
        if VectorFeature.objects.filter(query):
            raise serializers.ValidationError("Геометрия не должна пересекаться с другой")
        return value


class RestrictAreaValidator:
    def __init__(self, min_area, max_area):
        self.min_area = min_area
        self.max_area = max_area

    def __call__(self, value):
        if value.area < self.min_area or value.area > self.max_area:
            raise serializers.ValidationError(f"Площадь геометрии должна быть в пределах [{self.min_area}:{self.max_area}]")
        return value


    
