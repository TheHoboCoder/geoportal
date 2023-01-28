from django.urls import path
from .base_views import get_commands, run_command, ListAreaView, ListLayerView

base_urls = [
    path('get_commands', get_commands),
    path('run_command/<command_name>', run_command),
    path('area', ListAreaView.as_view()),
    path('layer', ListLayerView.as_view()),
] 