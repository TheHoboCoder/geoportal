from datetime import datetime

class AreaPO:
    def __init__(self, name: str, bbox: tuple, alias:str = ""):
        self.name = name
        self.bbox = bbox
        self.alias = alias

class LayerPO:
    def __init__(self, name: str, 
                       ordering: int, 
                       alias:str = "", 
                       area:str|None=None,
                       serializer_cls=None,
                       is_vector=True):
        self.name = name
        self.area = area
        self.alias = alias
        self.ordering = ordering
        self.serializer_cls = serializer_cls
        self.is_vector = is_vector

class FeaturePO:
    def __init__(self, name: str = "", date: datetime = None):
        self.name = name
        self.datetime = date

# векторные данные
class VectorFeaturePO(FeaturePO):
    def __init__(self, properties: dict, geometry: tuple, date: datetime = None):
        """

        Args:
            properties (dict): словарь примитивных типов python. Лучше не использовать вложенные словари
            geometry (tuple): список объектов векторной геометрии geos: https://docs.djangoproject.com/en/4.1/ref/contrib/gis/geos/#geometry-objects
            date (datetime, optional): дата. Defaults to None.
        """
        super().__init__(date)
        self.properties = properties
        self.geometry = geometry

class RasterFeaturePO(FeaturePO):
    def __init__(self, file, date: datetime = None):
        super().__init__(date)
        self.file = file
