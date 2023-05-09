from rest_framework import serializers
from common import serializers as geo_serializers

""" сериализаторы задают входные данные для команды
Поддерживаемые типы полей:
    Атрибутивная информация:
        - целые числа IntegerField
        - дробные числа FloatField
        - строки CharField
        - выбор из списка значений ChoiceField
    Пространственная информация:
        - точка PointField
        - линия LineStringField
        - полигон PolygonField

    Более подробная информация - см. документацию по Django Rest Framework / Serializers
"""
class DrawLineSerializer(serializers.Serializer):
    # для поля можно указать название, которое будет отображаться на форме
    # для числовых полей также можно задать минимальное и максимальное значение
    int_param = serializers.IntegerField(label="Количество", min_value=1, max_value=5)
    # для строковых - максимальную длину
    string_param = serializers.CharField(label="Введите test", max_length=50)
    point_start = geo_serializers.PointField()
    point_end = geo_serializers.PointField()

    # для поля можно задать алгоритм валидации
    def validate_string_param(self, val):
        if "test" not in val:
            raise serializers.ValidationError("string_param should contain 'test' word")
        return val
    
class StylingPrimerSerializer(serializers.Serializer):
    polygon = geo_serializers.PolygonField(label="Полигон")

class OverpassAPISerializer(serializers.Serializer):
    bbox_left = geo_serializers.PointField(label="Верхний угол")
    bbox_right = geo_serializers.PointField(label="Нижний угол")




    