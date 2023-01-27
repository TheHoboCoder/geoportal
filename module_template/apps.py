from django.apps import AppConfig
from geoportal.geoserver import get_geoserver, install_module
import os

class ModuleTemplateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'module_template'

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            # install_module(get_geoserver(), self.label, self.get_models())
            pass
