from django.db import models
from django.contrib.auth.models import User
  
class Module(models.Model):
    """ Модуль для установки
    """
    name = models.SlugField(max_length=15, primary_key=True)
    alias = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.RESTRICT)











    


