from django.db import models
from django.contrib.gis.db import models as gis_models
from .base.base_models import *

class SomeGISModel(models.Model):
    int_property = models.IntegerField()
    point_field = gis_models.PointField()

    class Meta:
        gis_model = True
        layer_name = 'gis_model'

