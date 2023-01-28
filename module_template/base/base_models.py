
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.db import models
from django.contrib.gis.geos import Point

class Area(models.Model):
    """ Именнованая прямоугольная область на карте, к которой могут быть привязаны
        различные гео объекты.
    """
    name = models.SlugField(max_length=15)
    alias = models.CharField(max_length=50)
    # Point(xmin, ymin), Point(xmax, ymax)
    point_min = gis_models.PointField(default=Point(33, 65))
    point_max = gis_models.PointField(default=Point(34, 66))

class Layer(models.Model):
    name = models.SlugField(max_length=15)
    # если area = Null, то слой виден во всех областях, иначе только в конкретной области
    area = models.ForeignKey(Area, on_delete=models.CASCADE, blank=True, null=True)
    alias = models.CharField(max_length=50, blank=True)
    ordering = models.IntegerField(max_length=5, default=0)
    layer_type = models.CharField(max_length=1, choices=(('V', 'Vector'), ('R', 'Raster')), default='V')

class GISModel(models.Model):
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        abstract = True

class RasterFeature(GISModel):
    r_file = models.FilePathField()