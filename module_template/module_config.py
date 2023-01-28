from .views import ExampleView
from .base.base_models import Area, Layer
from django.contrib.gis.geos import Point
from .models import SomeGISModel

COMMANDS = {
    "do_some": ExampleView()
}

AREAS = {
    'layers': [
        (Layer(name="ground_layer", alias="Векторный слой"), SomeGISModel)
    ],
    'areas': [Area(name="main_area", alias="Основная область", point_min=Point((33, 65)), point_max=Point((35, 66)))]
}