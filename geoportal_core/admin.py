from django.contrib import admin
from . import models

admin.site.register(models.GISModule)
admin.site.register(models.Layer)
admin.site.register(models.Area)
admin.site.register(models.VectorFeature)


