from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point, Polygon, GeometryCollection
from django.db import transaction
from django.db.models import Q
from common import models as c_models
from common.internal.modules import MODULES
    
class GISModule(models.Model):
    """ Модуль для установки
    """
    name = models.SlugField(max_length=15, unique=True, verbose_name="Название")
    alias = models.CharField(max_length=50, verbose_name="Псевдоним")
    summary = models.CharField(max_length=100, verbose_name="Краткое описание")
    description = models.TextField(verbose_name="Описание", blank=True)
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, verbose_name="Разработчик")

    def __str__(self) -> str:
        return f"Модуль {self.name}"
    
    def owner_name(self):
        return self.owner.get_full_name()
    
    @transaction.atomic
    def import_data(self):
        schema = MODULES[self.name].schema
        for area in map(lambda t: Area.from_po(po=t, module=self), schema.areas):
            area.save()
        for layer in schema.layers:
            layer_model = Layer.from_po(po=layer, module=self)
            layer_model.save()
            if layer.layer_content is not None:
                if layer.is_vector:
                    for feature in layer.layer_content.get_objects():
                        VectorFeature.from_po(feature, layer_model, layer_model.area).save()
                else:
                    for feature in layer.layer_content.raster_objects:
                        po = RasterFeature.from_po(feature, layer_model, layer_model.area)
                        #TODO: extension
                        po.raster_file.save(f"{self.name}/rasters/{po.name}.png", feature.file, save=True)
                        po.save()  

    def save(self, *args, **kwargs):
        is_created = self.pk is None
        super(GISModule, self).save()
        if is_created:
            self.import_data()

    def remove_mod(self):
        MODULES.remove_module(self.name)
            
    class Meta:
        verbose_name = "Модуль"

def get_areas(args):
    return Q(module__name=args["module_name"])

class AreaManager(models.Manager):
    def path_filter(self, args):
        return self.filter(get_areas(args)) 
        
class Area(models.Model):
    """ Именнованая прямоугольная область на карте, к которой могут быть привязаны
        различные гео объекты.
    """
    name = models.SlugField(verbose_name="Название", max_length=15)
    alias = models.CharField(verbose_name="Псевдоним", max_length=50)
    module = models.ForeignKey(GISModule, on_delete=models.CASCADE, verbose_name="Модуль")
    # Point(xmin, ymin), Point(xmax, ymax)
    bbox = gis_models.PolygonField(default=Polygon.from_bbox((33, 65, 35, 66)), verbose_name="Ограничивающий прямоугольник")
    objects = AreaManager()

    def __str__(self) -> str:
        return f"Область {self.name}, {self.module.name}"

    @classmethod
    def from_po(cls, po: c_models.AreaPO, module):
        return cls(name=po.name, 
                    module=module,
                    alias=po.alias, 
                    bbox=Polygon.from_bbox(po.bbox))
    
    def to_po(self):
        return c_models.AreaPO(name=self.name, alias=self.alias, bbox=self.bbox.extent)

    class Meta:
        unique_together = ['name', 'module']
        verbose_name = "Область"

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
    name = models.SlugField(max_length=15, verbose_name="Название")
    # если area = Null, то слой виден во всех областях, иначе только в конкретной области
    area = models.ForeignKey(Area, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Область")
    module = models.ForeignKey(GISModule, on_delete=models.CASCADE, verbose_name="Модуль")
    alias = models.CharField(max_length=50, verbose_name="Псевдоним")
    ordering = models.IntegerField(default=0, verbose_name="Положение")
    layer_type = models.CharField(max_length=1, choices=(('V', 'Vector'), ('R', 'Raster')), default='V', verbose_name="Тип")
    objects = LayerManager()

    def is_vector(self):
        return self.layer_type == 'V'

    @classmethod
    def from_po(cls, po: c_models.LayerPO, module):
        return cls(name=po.name,
                    area=None if not po.area else Area.objects.get(name=po.area, module=module),
                    alias=po.alias,
                    ordering=po.ordering,
                    module=module,
                    layer_type='V' if po.is_vector else 'R')
    
    def __str__(self) -> str:
        type_l = "Векторный" if self.layer_type == 'V' else "Растровый"
        return f"{type_l} cлой {self.name}, {self.module.name}"

    class Meta:
        unique_together = ['name', 'module']
        ordering = ['ordering']
        verbose_name = "Слой"

class FeatureManager(models.Manager):
    def filter_features(self, module_name, layer_name, area_name):
        return self.filter(Q(area__module__name=module_name) &
                           Q(layer__name=layer_name) &
                           Q(area__name=area_name))
    
    def datetime_filter(self, queryset, datetime_start, datetime_end=None):
        datetime_end = datetime_end if datetime_end is not None else datetime_start
        return queryset.filter(Q(datetime__isnull=True) | 
                              (Q(datetime__gte=datetime_start) &
                               Q(datetime__lte=datetime_end)))
    
class Feature(models.Model):
    name = models.CharField(max_length=50, blank=True, verbose_name="Название")
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE, verbose_name="Слой")
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name="Область")
    datetime = models.DateTimeField(blank=True, null=True, verbose_name="Метка времени")
    objects = FeatureManager()

    def __str__(self) -> str:
        return f"Объект {self.name} слоя {self.layer.name}"

    class Meta:
        abstract = True

class VectorFeature(Feature):
    properties = models.JSONField(verbose_name="Атрибуты")
    geometry = gis_models.GeometryCollectionField(verbose_name="Геометрия")

    @classmethod
    def from_po(cls, po: c_models.VectorFeaturePO, layer, area):
        return cls(name=po.name,
                   layer=layer, 
                   area=area, 
                   datetime=po.date,
                   properties=po.properties,
                   geometry=GeometryCollection(po.geometry))
    
    def to_po(self):
        return c_models.VectorFeaturePO(name=self.name, 
                                        properties=self.properties, 
                                        geometry=tuple(self.geometry))
    
    class Meta:
        verbose_name = "Векторные объекты"

class RasterFeature(Feature):
    extent = gis_models.PolygonField(verbose_name="Ограничивающий прямоугольник", null=True)
    raster_file = models.ImageField(verbose_name="Файл")

    @classmethod
    def from_po(cls, po: c_models.RasterFeaturePO, layer, area):
        return cls(name=po.name,
                   layer=layer, 
                   area=area, 
                   datetime=po.date,
                   extent=Polygon.from_bbox(po.extent))


    











    


