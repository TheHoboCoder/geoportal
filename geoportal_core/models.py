from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
import importlib
from django.db import transaction

class GISModule(models.Model):
    """ Модуль для установки
    """
    name = models.SlugField(max_length=15, unique=True, verbose_name="Название")
    alias = models.CharField(max_length=50, verbose_name="Псевдоним", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, verbose_name="Разработчик")

    def __str__(self) -> str:
        return self.name

    @transaction.atomic
    def save(self, *args, **kwargs):
        super(GISModule, self).save()
        importlib.invalidate_caches()
        config = importlib.import_module(f"{self.name}.module_config", package=None)
        schema = config.SCHEMA
        for area_po in schema.areas:
            min_p, max_p = area_po.bbox
            area = Area(name=area_po.name, 
                        module=self,
                        alias=area_po.alias, 
                        point_min=Point(min_p),  
                        point_max=Point(max_p))
            area.save()
        for layer_po in schema.layers:
            layer = Layer(name=layer_po.name,
                          alias=layer_po.alias,
                          ordering=layer_po.ordering,
                          module=self,
                          layer_type='V' if layer_po.model_cls is not None else 'R')
            layer.save()
            if layer_po.model_cls is not None:
                layer_index = VectorLayerIndex(layer=layer, model_name=layer_po.model_cls.__name__)
                layer_index.save()
       
        
class Area(models.Model):
    """ Именнованая прямоугольная область на карте, к которой могут быть привязаны
        различные гео объекты.
    """
    name = models.SlugField(max_length=15)
    alias = models.CharField(max_length=50)
    module = models.ForeignKey(GISModule, on_delete=models.CASCADE)
    # Point(xmin, ymin), Point(xmax, ymax)
    point_min = gis_models.PointField(default=Point(33, 65))
    point_max = gis_models.PointField(default=Point(34, 66))

    class Meta:
        unique_together = ['name', 'module']

class Layer(models.Model):
    name = models.SlugField(max_length=15)
    # если area = Null, то слой виден во всех областях, иначе только в конкретной области
    area = models.ForeignKey(Area, on_delete=models.CASCADE, blank=True, null=True)
    module = models.ForeignKey(GISModule, on_delete=models.CASCADE)
    alias = models.CharField(max_length=50, blank=True)
    ordering = models.IntegerField(default=0)
    layer_type = models.CharField(max_length=1, choices=(('V', 'Vector'), ('R', 'Raster')), default='V')

    class Meta:
        unique_together = ['name', 'module']
        ordering = ['ordering']

class VectorLayerIndex(models.Model):
    """Связывает векторный слой и название модели"""
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE) 
    model_name = models.CharField(max_length=50)

class RasterFeature(models.Model):
    name = models.SlugField(max_length=15)
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    alias = models.CharField(max_length=50, blank=True)
    raster_filepath = models.FilePathField()











    


