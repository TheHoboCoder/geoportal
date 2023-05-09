from django.shortcuts import render
from django.contrib.gis.geos import LineString, Point, Polygon
from .serializers import DrawLineSerializer, StylingPrimerSerializer, OverpassAPISerializer
from common.commands import CommandResponse, CommandView
from common.models import LayerPO, VectorFeaturePO, VectorLayerContent, URLLayerContent, Formats
from common.styling import VectorStyle, FillStyle, StrokeStyle, CirclePointStyle
from common.utils import RangeConverter, create_overpass_query


# пример простой команды
class DrawLineView(CommandView):
    serializer_class = DrawLineSerializer
    name="draw_line_command"
    description = "Рисует линию между двумя точками"
    alias = "Рисование линии"

    def handler(self, validated_data):
        layers = [
            LayerPO(name="layer_1",
                    alias="Результат выполнения команды",
                    # пример использования нескольких стилей:
                    # будем использовать две обводки для линии, чтобы 
                    # сделать сердцевину одного цвета, а края - другого
                    styles=[
                        VectorStyle(
                            stroke=StrokeStyle("yellow", 5)
                        ),
                        VectorStyle(
                            stroke=StrokeStyle("blue", 1.2),
                            point_style=CirclePointStyle(4, fill=FillStyle('red'), stroke=None)
                        ),
                    ],
                    layer_content=[
                        VectorFeaturePO(
                            name="res",
                            properties={"line": validated_data['int_param']},
                            geometry=(
                                LineString(validated_data['point_start'], validated_data['point_end']),
                                validated_data['point_start'],
                                validated_data['point_end']
                            )
                        )
                    ]
            )
        ]
        return CommandResponse(layers=layers, custom_data={
            'msg': f"{validated_data['string_param']} has some {validated_data['int_param']} in it. Awesome"
        })
    

# пример использования вычисляемых стилей
# на вершинах полигона создадим окружности, цвет которых будет меняться от синего до красного
# в зависимости от их порядкого номера
class StylingPrimerView(CommandView):
    serializer_class = StylingPrimerSerializer
    name="primer_style_command"
    description = "пример использования вычисляемых стилей"
    alias = "пример стилей"
    # цвет в hsl, чтобы сделать обводку чуть темнее
    COLOR_START = (217, 75, 39)
    COLOR_END = (344, 68, 39)

    def handler(self, validated_data):
        polygon = validated_data["polygon"]
        # создаем шкалу цвета с помощью класса RangeConverter
        color_scale = RangeConverter([((0, len(polygon.coords[0]) - 1),
                                       (self.COLOR_START, self.COLOR_END))])
        # задаем функцию для вычисления стиля
        def style_function(featurePO):
            clr = color_scale.convert(featurePO.properties["index"])
            return [
                VectorStyle(point_style=CirclePointStyle(
                                        radius=6, 
                                        fill=FillStyle(f"hsl({clr[0]} {clr[1]}% {clr[2]}% / 60%)"),
                                        stroke=StrokeStyle(f"hsl({clr[0]} {clr[1]}% {clr[2] - 10}%)", 2)
                                    ))
            ]
        
        # создаем контент слоя и указываем функцию для указания стиля
        vector_content = VectorLayerContent((), styling_function=style_function)

        #создаем объекты
        for i, coord in enumerate(polygon.coords[0]):
            vector_content.add_object(VectorFeaturePO(f"point_{i}", 
                                                      {"index": i},
                                                      (Point(coord))))
            
        return CommandResponse(
            [LayerPO(name="t", alias="Пример стилей", layer_content=vector_content)],
            {}
        )

# пример загрузки данных слоя из внешних источников (в данном случае - OverpassAPI)   
class OverpassPrimerView(CommandView):
    serializer_class = OverpassAPISerializer
    name="primer_overpass_command"
    description = "пример использования OverpassAPI"
    alias = "Overpass API"

    def handler(self, validated_data):
        x_s = sorted((validated_data["bbox_left"][0], validated_data["bbox_right"][0]))
        y_s = sorted((validated_data["bbox_left"][1], validated_data["bbox_right"][1]))
        bounding_poly = Polygon.from_bbox((x_s[0], y_s[0], x_s[1], y_s[1]))
        overpass_bbox = f"({y_s[0]}, {x_s[0]}, {y_s[1]}, {x_s[1]})"
        # выборка из Overpass данных о лесах
        overpass_query = f"""
            (
                relation[natural=wood]{overpass_bbox};
                relation[landuse=forest]{overpass_bbox};
            );
        """
        
        return CommandResponse([

            LayerPO(name="overpass_l", 
                    alias="Вывод overpass",
                    layer_content=URLLayerContent(
                        url=create_overpass_query(overpass_query),
                        format=Formats.OVERPASS
                    )),

            LayerPO(name="bounding_box", 
                    alias="Ограничивающий прямоугольник",
                    styles=[
                        VectorStyle(stroke=StrokeStyle("yellow", 2))
                    ],
                    layer_content=[
                        VectorFeaturePO("bbox", {"a": 1}, (bounding_poly))
                    ])
            
        ], {})








