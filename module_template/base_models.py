
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.db import models

#TODO: ugly
models.options.DEFAULT_NAMES += ('gis_model', 'layer_name')

class Area(models.Model):
    """ Именнованая прямоугольная область на карте, к которой могут быть привязаны
        различные гео объекты.
    """
    name = models.SlugField(max_length=15)
    alias = models.CharField(max_length=50)
    # Point(xmin, ymin), Point(xmax, ymax)
    bbox = gis_models.MultiPointField()

class Layer(models.Model):
    name = models.SlugField(max_length=15)
    # если area = Null, то слой виден во всех областях, иначе только в конкретной области
    area = models.ForeignKey(Area, on_delete=models.CASCADE, blank=True, null=True)
    alias = models.CharField(max_length=50)
    ordering = models.IntegerField(max_length=5)
    layer_type = models.CharField(max_length=1, choices=(('V', 'Vector'), ('R', 'Raster')))

class RasterFeature(models.Model):
    name = models.SlugField(max_length=15)
    r_file = gis_models.RasterField()