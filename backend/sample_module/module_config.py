from .views import DrawLineView, StylingPrimerView, OverpassPrimerView
from common.models import AreaPO, LayerPO, FileLayerContent
from common.commands import CommandList
from common.schema import Schema
from common.styling import VectorStyle, FillStyle, StrokeStyle
from pathlib import Path
import os

COMMANDS = CommandList(
    (DrawLineView(),
     StylingPrimerView(),
     OverpassPrimerView()
    #other command
    )
)

# путь к папке с файлами
PATH = os.path.join(Path(__file__).resolve().parent, "assets")

SCHEMA = Schema(

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

            # пример импорта векторных данных из файлов
            LayerPO(name="import_json",
                    ordering=3,
                    alias="Импортированный слой",
                    # для импортированных слоев обязательно нужно указывать area
                    area="hibins",
                    layer_content=FileLayerContent(PATH+"/sample_geojson.json")
                    ),

            # для файлов, которые содержат несколько слоев, можно указать номер слоя
            # c помощью параметра layer_index
            #  или импортировать все слои при помощи метода read_all_layers()
            #  (в этом случае надо их добавить к существующим слоям при помощи .extend())

            LayerPO(name="import_sph",
                    ordering=4,
                    alias="Импортированный слой 2",
                    area="hibins",
                    layer_content=FileLayerContent(PATH+"/shapefile/sample_shapefile.shp")
                    ),


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
