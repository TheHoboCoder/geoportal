from django.db import models
from django.contrib.gis.db import models as gis_models
from common.models import GISModel

class SomeGISModel(GISModel):
    int_property = models.IntegerField()
    point_field = gis_models.PointField()

