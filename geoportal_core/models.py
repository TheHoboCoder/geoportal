from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point, Polygon, GeometryCollection
import importlib
from django.db import transaction
import importlib
from django.db.models import Q
from common import models as c_models
    
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
        if self.pk is None:
            importlib.invalidate_caches()
            config = importlib.import_module(f"{self.name}.module_config", package=None)
            schema = config.SCHEMA
            for area in map(lambda t: Area.from_po(po=t, module=self), schema.areas):
                area.save()
            for layer in map(lambda t: Layer.from_po(po=t, module=self), schema.layers):
                layer.save()

    class Meta:
        verbose_name = "модуль"

def get_areas(args):
    return Q(module__name=args["module_name"])

class AreaManager(models.Manager):
    def path_filter(self, args):
        return self.filter(get_areas(args)) 
        
class Area(models.Model):
    """ Именнованая прямоугольная область на карте, к которой могут быть привязаны
        различные гео объекты.
    """
    name = models.SlugField(max_length=15)
    alias = models.CharField(max_length=50)
    module = models.ForeignKey(GISModule, on_delete=models.CASCADE)
    # Point(xmin, ymin), Point(xmax, ymax)
    bbox = gis_models.PolygonField(default=Polygon.from_bbox((33, 65, 35, 66)))
    objects = AreaManager()

    @classmethod
    def from_po(cls, po: c_models.AreaPO, module):
        return cls(name=po.name, 
                    module=module,
                    alias=po.alias, 
                    bbox=Polygon.from_bbox(po.bbox))

    class Meta:
        unique_together = ['name', 'module']

def get_layers(args):
    return get_areas(args) & (Q(area__name__isnull=True) | 
                              Q(area__name=args["area_name"]))

def get_layer_content(args):
    return Q(name=args["layer_name"]) & get_layers(args)

class LayerManager(models.Manager):
    def path_filter(self, args):
        return self.filter(get_layers(args))
    
    def path_get(self, args):
        return self.get(get_layer_content(args))

class Layer(models.Model):
    name = models.SlugField(max_length=15)
    # если area = Null, то слой виден во всех областях, иначе только в конкретной области
    area = models.ForeignKey(Area, on_delete=models.CASCADE, blank=True, null=True)
    module = models.ForeignKey(GISModule, on_delete=models.CASCADE)
    alias = models.CharField(max_length=50, blank=True)
    ordering = models.IntegerField(default=0)
    layer_type = models.CharField(max_length=1, choices=(('V', 'Vector'), ('R', 'Raster')), default='V')
    objects = LayerManager()

    def is_vector(self):
        return self.layer_type == 'V'

    @classmethod
    def from_po(cls, po: c_models.LayerPO, module):
        return cls(name=po.name,
                    area=None if not po.area else Area.objects.get(name=po.area),
                    alias=po.alias,
                    ordering=po.ordering,
                    module=module,
                    layer_type='V' if po.is_vector else 'R')

    class Meta:
        unique_together = ['name', 'module']
        ordering = ['ordering']

class FeatureManager(models.Manager):
    def filter_features(self, layer_name, area_name):
        return self.filter(Q(layer__name=layer_name) &
                        Q(area__name=area_name))
    
    def datetime_filter(self, queryset, datetime_start, datetime_end=None):
        datetime_end = datetime_end if datetime_end is not None else datetime_start
        return queryset.filter(Q(datetime__isnull=True) | 
                           (Q(datetime__gte=datetime_start) &
                            Q(datetime__lte=datetime_end)))
    
class Feature(models.Model):
    name = models.CharField(max_length=50, blank=True)
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    datetime = models.DateTimeField(blank=True, null=True)
    objects = FeatureManager()

    class Meta:
        abstract = True

class VectorFeature(Feature):
    properties = models.JSONField()
    geometry = gis_models.GeometryCollectionField()

    @classmethod
    def from_po(cls, po: c_models.VectorFeaturePO, layer, area):
        return cls(name=po.name,
                   layer=layer, 
                   area=area, 
                   datetime=po.datetime,
                   properties=po.properties,
                   geometry=GeometryCollection(po.geometry))

class RasterFeature(Feature):
    raster_filepath = models.FilePathField()










    


