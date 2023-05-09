from .views import DrawLineView, StylingPrimerView, OverpassPrimerView
from common.models import AreaPO, LayerPO
from common.commands import CommandList
from common.schema import Schema
from common.styling import VectorStyle, FillStyle, StrokeStyle

COMMANDS = CommandList(
    (DrawLineView(),
     StylingPrimerView(),
     OverpassPrimerView()
    #other command
    )
)

SCHEMA = Schema(

 # TODO: импортирование областей из geojson / shapefile
    areas=(AreaPO(name="hibins", 
                  alias="Хибины", 
                  bbox=(32.7172, 67.3483, 34.6289,  67.97463)),

           AreaPO(name="murmansk", 
                  alias="Мурманск", 
                  bbox=(32.71728, 68.897, 34.3542, 69.37257)),

           AreaPO(name="lake", 
                  alias="Водохранилище", 
                  bbox=(30.48706, 68.2449, 32.124, 68.78)),
           #other area
           ),

    # Для слоя можно указать стиль или функцию для вычисления стиля
    layers=(LayerPO(name="ground_layer",
                    ordering=0,
                    alias="Векторный слой 1",
                    styles=[
                        VectorStyle(fill=FillStyle('rgba(131, 122, 235, 0.4)'),
                                    stroke=StrokeStyle('rgb(131, 122, 235)', 2))
                     ]), 

            LayerPO(name="vector_layer_1",
                    ordering=1,
                    alias="Векторный слой 2"), 

            LayerPO(name="specific_layer",
                    area="murmansk",
                    ordering=2,
                    alias="Слой, доступный в одной области")
            # other layer
            )
)
