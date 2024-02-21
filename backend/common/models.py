from datetime import datetime
from abc import ABC, abstractmethod
from django.contrib.gis.gdal.datasource import DataSource
import requests
import enum
from django.core.files.base import ContentFile
from .utils import RangeConverter
from io import BytesIO
import numpy as np
from PIL import Image

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

# TODO: areas
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
    """Растровые пространственные данные
    """
    def __init__(self, 
                 name: str,
                 extent, 
                 file: ContentFile, 
                 date: datetime = None):
        """
        Args:
            name (str): Название
            extent (область): формат (xmin, ymin, xmax, ymax)
            file (ImageFile): файл с изображением
            date (datetime, optional): дата и время. Defaults to None.
        """
        super().__init__(name, date)
        self.extent = extent
        self.file = file

    @staticmethod
    def image_from_data(color_converter: RangeConverter, 
                        data_matrix: np.array,
                        image_mode: str,
                        min_val: int,
                        max_val: int) -> ContentFile:
        """Cоздает ImageFile из матрицы данных data_matrix. 
            Значения в матрице будут заменены на цвет согласно color_converter.
            Для ускорения работы все значения в матрице округляются и приводятся к int.
            Изображение будет создано в формате .png

        Args:
            color_converter (RangeConverter): шкала цвета.
            data_matrix (np.array): матрица numpy
            image_mode (str): Режим изображения: RGB, RGBA, HSV, ... (cм. Pillow/Modes)
                NOTE: размерность возвращаемого color_converter значения должна соотвествовать режиму
            min_val (int): Минимально возможное значение в data_matrix
            max_val (_type_): Максимально возможное значение в data_matrix

        Returns:
            ImageFile: файл изображения
        """
        pallete = np.array([color_converter.convert(val) for val in range(min_val, max_val+1)])
        res = pallete[(np.round(data_matrix).flatten() - min_val).astype(int)]
        # putdata не хочет принимать np.array, нужно его предварительно сконвертировать в обычный список
        res = np.round(res).astype(int).T
        res = list(zip(*res))
        image = Image.new(image_mode, data_matrix.shape[::-1])
        image.putdata(res)
        if image_mode != 'RGB' and image_mode != 'RGBA':
            image = image.convert('RGB')
        buffer = BytesIO()
        image.save(buffer, format='png')
        image.close()
        image_file = ContentFile(buffer.getvalue())
        buffer.close()
        return image_file
        


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
            layer_content (BaseVectorLayerContent|RasterLayerContent|None): Контент слоя
                Может быть подклассом BaseVectorLayerContent, RasterLayerContent или списком объектов VectorFeaturePO.
                В последнем случае автоматически будет создан VectorLayerContent
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

#TODO: refactor
class RasterLayerContent:
    def __init__(self, raster_objects, styling_function=None):
        self.raster_objects = raster_objects
        self.styling_function = styling_function
         
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
    def __init__(self, 
                 format=Formats.GEOJSON, 
                 srid=4326, 
                 layer_index=0,
                 styling_function=None,):
        """
        Args:
            format (Formats, optional): формат. Defaults to Formats.GEOJSON.
            srid (int, optional): Код проекции данных. По дефолту 4326 - неспроецированные данные.
            layer_index (int): индекс слоя (для форматов, поддерживающих несколько слоев). Дефолт: 0
        """
        super().__init__(styling_function)
        self.format = format
        self.srid = srid
        self.__converted = []
        self.layer_index = layer_index

    @abstractmethod
    def get_data_source(self) -> DataSource:
        if self.format == Formats.OVERPASS:
            raise NotImplementedError("reading overpass on back-end is currently not supported")

    def convert(self, layer):
        res = []
        for feature in layer:
            properties = {field.name: field.value for field in feature}
            feature_name = f"{feature.layer_name}_{feature.fid}"
            # TODO: datetime 
            if "name" in properties:
                feature_name = properties["name"]
                del properties["name"]
            geometry = (feature.geom.geos, )
            if feature.geom_type == 'GeometryCollection':
                geometry = tuple(feature.geom.geos)
            res.append(VectorFeaturePO(feature_name, properties, geometry))
        return res
    
    # читает все слои и возвращает список LayerPO
    def read_all_layers(self):
        ds = self.get_data_source()
        res = []
        for i in range(0, ds.layer_count):
            res.append(LayerPO(
                name=ds[i].name,
                styling_function=self.styling_function,
                layer_content=self.convert(ds[i])
            ))
        return res
        
    def get_objects(self):
        if len(self.__converted) == 0:
            self.__converted = self.convert(self.get_data_source()[self.layer_index])
        return self.__converted


class URLLayerContent(ExternalLayerContent):
    def __init__(self, url: str, 
                 format=Formats.GEOJSON, 
                 srid=4326, 
                 layer_index=0,
                 styling_function=None):
        """
        Векторные данные, доступные по url
        """
        super().__init__(format, srid, layer_index, styling_function)
        self.url = url

    def get_data_source(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"can't access {self.url}: status {response.status_code}")
        return DataSource(response.text)
    
class FileLayerContent(ExternalLayerContent):
    def __init__(self, file_path: str, 
                 format=Formats.GEOJSON, 
                 srid=4326, 
                 layer_index=0,
                 styling_function=None):
        """
        Векторные данные, доступные по url
        """
        super().__init__(format, srid, layer_index, styling_function)
        self.file_path = file_path

    def get_data_source(self):
        super().get_data_source()
        return DataSource(self.file_path)




