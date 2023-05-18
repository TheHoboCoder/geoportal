from datetime import datetime
from abc import ABC, abstractmethod
import enum

class FeaturePO:
    """
    Базовый класс для пространственных данных
    """
    def __init__(self, name: str, date: datetime = None):
        """
        Args:
            name (str): Название
            date (datetime, optional): Метка времени. Defaults to None.
        """
        self.name = name
        self.date = date


class VectorFeaturePO(FeaturePO):
    def __init__(self, 
                 name: str, 
                 properties: dict, 
                 geometry: tuple,
                 styles = None,
                 styling_function = None, 
                 date: datetime = None):
        """
        Векторные пространственные данные

        Args:
            name (str): Название
            properties (dict): атрибуты, словарь примитивных типов python. 
                    Лучше не использовать вложенные словари
            geometry (tuple): список объектов векторной геометрии geos:
               https://docs.djangoproject.com/en/4.1/ref/contrib/gis/geos/#geometry-objects
            styles (tuple|list of VectorStyle): список объектов VectorStyle,
                    стили отображения геометрии. (см. styling.py)
                    (Для объекта можно указать несколько стилей)
            styling_function: функция для вычисления стилей. 
                    Принимает объект VectorFeaturePO, должна вернуть список VectorStyle.
                    Если одновременно указаны и стили и функция, то стили будет перезаписаны.
            date (datetime, optional): дата и время. Defaults to None.
        """
        super().__init__(name, date)
        self.properties = properties
        self.geometry = geometry
        self.styles = styles
        self.styling_function = styling_function 

    def apply_style(self):
        if self.styling_function is not None:
            self.styles = self.styling_function(self)

class RasterFeaturePO(FeaturePO):
    """Растровые пространственные данные (в разработке)
    """
    def __init__(self, file, date: datetime = None):
        super().__init__(date)
        self.file = file

class AreaPO:
    def __init__(self, name: str, bbox: tuple, alias:str = ""):
        """Именнованая прямоугольная область на карте, 
        к которой могут быть привязаны слои и пространственные объекты.

        Args:
            name (str): идентификатор модуля, строка, 
                содержащая только латинские буквы, цифры и символ подчеркивания.
                Должен быть уникальным
            bbox (tuple): массив координат, задающих прямоугольник: 
                (долгота-мин, широта-мин, долгота-макс, широта-макс)
            alias (str, optional): Отображаемое имя модуля. Defaults to "".
        """
        self.name = name
        self.bbox = bbox
        self.alias = alias

class LayerPO:
    def __init__(self, name: str, 
                       ordering:int=0, 
                       alias:str="", 
                       area=None,
                       is_vector=True,
                       styles=None,
                       styling_function=None,
                       layer_content=None):
        """Слой

        Args:
            name (str): идентификатор слоя - строка, 
                содержащая только латинские буквы, цифры и символ подчеркивания.
                Должен быть уникальным
            ordering (int): положение слоя, отсчитывается сверху вниз (0 - самый верхний).
                Имеет смысл только при сохранении слоя в БД. Defaults to 0.
            alias (str, optional): Отображаемое имя слоя. Defaults to "".
            area (str, optional): Идентификатор области. Если указан, то
                слой будет виден только в данной области, 
                в противном случае - во всех областях.
                Defaults to None.
            is_vector (bool, optional): Тип слоя - векторный(True) или растровый(False).
                Defaults to True.
            style(VectorStyle) - стиль слоя. Будет использован, 
                если для векторных объектов в layer_content не указан свой стиль и styling_function.
            styling_function - Функция для вычисления стиля. 
                Если у layer_content она не указана, то будет к нему применена
            layer_content (BaseVectorLayerContent|None): Контент слоя
                Может быть подклассом BaseVectorLayerContent или списком объектов VectorFeaturePO.
                Во втором случае автоматически будет создан VectorLayerContent
        """
        self.name = name
        self.area = area
        self.alias = alias
        self.ordering = ordering
        self.is_vector = is_vector
        self.styles = styles
        if isinstance(layer_content, (tuple, list)):
           layer_content = VectorLayerContent(layer_content, styling_function)
        self.styling_function = styling_function
        self.layer_content = layer_content
        if self.layer_content is not None and self.layer_content.styling_function is None:
            self.layer_content.styling_function = styling_function

    def get_styling_function(self):
        if self.styling_function is not None:
            return self.styling_function
        if self.layer_content is not None:
            return self.layer_content.styling_function
        return None

class BaseVectorLayerContent(ABC):
    def __init__(self, styling_function=None):
        self.styling_function = styling_function

    @abstractmethod
    def get_objects(self):
        pass
    
    def apply_style(self, obj):
        if obj.styling_function is None:
            obj.styling_function = self.styling_function
        
        obj.apply_style()

    # применяет стиль для векторных объектов
    def apply_styles(self):
        for vector_object in self.get_objects():
            self.apply_style(vector_object)

    
class VectorLayerContent(BaseVectorLayerContent):
    def __init__(self, vector_objects, styling_function=None):
        """Базовый контент слоя

        Args:
            vector_objects (tuple | list): список объектов VectorFeaturePO
            styling_function (function, optional): Функция для вычисления стиля. 
                В нее передается объект VectorFeaturePO, она должна вернуть VectorStyle.
                Эта функция будет применятся ко всем vector_objects, 
                у которых не указана собственная styling_function.
            Defaults to None.
        """
        super().__init__(styling_function)
        self.__vector_objects = list(vector_objects)
        self.apply_styles()

    @property
    def vector_objects(self):
        return self.__vector_objects
    
    def get_objects(self):
        return self.__vector_objects
    
    @vector_objects.setter
    def vector_objects(self, value):
        self.__vector_objects = value
        self.apply_styles()

    def add_object(self, vector_object):
        self.apply_style(vector_object)
        self.__vector_objects.append(vector_object)

class Formats(enum.Enum):
    GEOJSON = 'geojson'
    GML = 'gml'
    OVERPASS = 'overpass'

class ExternalLayerContent(BaseVectorLayerContent, ABC):
    """
    Контент слоя, который хранится в заданном формате во внешних источниках (url, файл и тд.)
    """
    def __init__(self, format=Formats.GEOJSON, srid=4326, styling_function=None):
        """
        Args:
            format (Formats, optional): формат. Defaults to Formats.GEOJSON.
            srid (int, optional): Код проекции данных. По дефолту 4326 - неспроецированные данные.
        """
        super().__init__(styling_function)
        self.format = format
        self.__converted = []
        self.srid = srid

    # загружает данные и преобразовывает их в список VectorFeature
    @abstractmethod
    def convert(self):
        pass

    def get_objects(self):
        if len(self.__converted) == 0:
            self.__converted = self.convert()
        return self.__converted 


class URLLayerContent(ExternalLayerContent):
    def __init__(self, url: str, format=Formats.GEOJSON, srid=4326):
        """
        Векторные данные, доступные по url
        """
        super().__init__(format, srid)
        self.url = url

    def convert(self):
        # TODO: загрузка по url, конвертация
        raise NotImplementedError("в разработке")
    
#TODO: FileLayerContent




