from django.apps import AppConfig
from common.internal.modules import MODULES
import os
from django.conf import settings


class GeoportalCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'geoportal_core'

    def ready(self):
        with os.scandir(settings.MODULE_PATH) as it:
            for entry in it:
                if entry.is_dir() and \
                   entry.name != '__pycache__' and \
                   not entry.name.startswith('.') and \
                   not MODULES.contains(entry.name):
                    MODULES.install_module(entry.name)
        
