from django.db import models
from django.contrib.auth.models import User
  
class GISModule(models.Model):
    """ Модуль для установки
    """
    name = models.SlugField(max_length=15, unique=True, verbose_name="Название")
    alias = models.CharField(max_length=50, verbose_name="Псевдоним", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, verbose_name="Разработчик")

    def __str__(self) -> str:
        return self.name











    


