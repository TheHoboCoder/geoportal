from django.urls import path
from .base.base_views import get_commands

urlpatterns = [
    path('get_commands', get_commands),
] 