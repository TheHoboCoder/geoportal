class FillStyle:
    """
    Заливка фигуры
    """
    def __init__(self, color: str):
        """
        Args:
            color (str): CSS cтрока, задающая цвет:
                           - по названию
                           - по HEX коду
                           - по компонентам: rgb, hsl
                           Градиенты не поддерживаются
        """
        self.color = color

    def to_representation(self):
        return {'color': self.color}
        

class StrokeStyle:
    """
    Контур фигуры
    """
    def __init__(self, color: str, width: float):
        """
        Args:
            color (str): CSS cтрока, задающая цвет линии
            width (float): толщина линии
        """
        self.color = color
        self.width = width

    def to_representation(self):
        return {'color': self.color, 'width': self.width}


class CirclePointStyle:
    """
    Стиль точки, отображение в виде окружности
    """
    def __init__(self, 
                 radius: float, 
                 fill: FillStyle, 
                 stroke: StrokeStyle,
                 exact=False):
        """
        Args:
            radius (float): радиус окружности. 
                            Если exact=false, радиус задается в единицах проекции карты (Меркатор)
                            Иначе - в метрах, при этом вместо окружности будет создан многоугольник,
                            её приближающий (с 32 сторонами).
                            NOTE: так как в этом случае будет отображаться многоугольник, то стиль
                            заливки и обводки в VectorStyle будет перезаписан значениями, указаными в этом объекте
            fill (FillStyle): Стиль заливки
            stroke (StrokeStyle): Стиль контура
            exact (bool, optional): См. выше. Defaults to False.
        """
        self.radius = radius
        self.fill = fill
        self.stroke = stroke
        self.exact = exact
        
    def to_representation(self):
        return {'type': 'circle',
                'radius': self.radius, 
                'exact': self.exact,
                'stroke': None if self.stroke is None else self.stroke.to_representation(),
                'fill': None if self.fill is None else self.fill.to_representation()}


#TODO:
class IconPointStyle:
    """
    Стиль точки, отображение в виде изображения
    """
    pass


class VectorStyle:
    def __init__(self, fill=None, stroke=None, point_style=None):
        """Стиль векторной геометрии

        Args:
            fill (FillStyle|None): Заливка
            stroke (StrokeStyle|None): Контур
            point_style (CirclePointStyle|None, optional): Стиль точки. Defaults to None.
                        NOTE: применяется только к отдельным точкам, а не к вершинам полигона/линии
        """
        self.point_style = point_style
        self.fill = fill
        self.stroke = stroke

    def to_representation(self):
        return {'point_style': None if self.point_style is None else self.point_style.to_representation(), 
                'stroke': None if self.stroke is None else self.stroke.to_representation(),
                'fill': None if self.fill is None else self.fill.to_representation()}