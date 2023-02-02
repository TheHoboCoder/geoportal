from django.db import models

class AreaPO:
    def __init__(self, name: str, bbox: tuple, alias:str = ""):
        self.name = name
        self.bbox = bbox
        self.alias = alias

class LayerPO:
    def __init__(self, name: str, 
                       ordering: int, 
                       alias:str = "", 
                       area:str|None=None, 
                       model_cls:type=None):
        self.name = name
        self.area = area
        self.alias = alias
        self.ordering = ordering
        self.model_cls = model_cls

class GISModel(models.Model):

    @property
    def alias(self):
        return self.__str__()

    class Meta:
        abstract = True

class TimedGISModel(GISModel):
    data = models.DateTimeField()

    class Meta:
        abstract = True
