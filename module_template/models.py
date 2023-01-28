from django.db import models
from django.contrib.gis.db import models as gis_models
from .base.base_models import *

class SomeGISModel(GISModel):
    int_property = models.IntegerField()
    point_field = gis_models.PointField()

