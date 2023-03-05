from .views import ExampleView
from common.models import AreaPO, LayerPO
from common.commands import CommandList
from common.schema import Schema
from django.contrib.gis.geos import Point

COMMANDS = CommandList(
    (ExampleView(),
    #other command
    )
)

SCHEMA = Schema(

    areas=(AreaPO(name="main_area", 
                  alias="Основная область", 
                  bbox=((33, 65), (35, 66))),
           #other area
           ),

    layers=(LayerPO(name="ground_layer",
                    ordering=0,
                    alias="Векторный слой"), 
            # other layer
            )
)
