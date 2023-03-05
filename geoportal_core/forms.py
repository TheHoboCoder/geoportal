from django import forms
from .models import GISModule
import zipfile, os, shutil
from django.conf import settings
from django.apps import apps
from django.core import management
from collections import OrderedDict
from django.db import transaction

class GISModuleForm(forms.ModelForm):
    module_file = forms.FileField()

    class Meta:
        model = GISModule
        exclude = ['owner']

    def save(self, owner, commit: bool = True):
        module_file = self.cleaned_data['module_file']
        del self.cleaned_data['module_file']
        model = super().save(commit=False)
        model.owner = owner
        if commit:
            fullpath = os.path.join(settings.MODULE_PATH, self.cleaned_data['name'])
            try:
                unzip_file(module_file, self.cleaned_data['name'], fullpath)
                model.save()
            except Exception:
                if os.path.exists(fullpath):
                    shutil.rmtree(fullpath)
                raise Exception
        return model

def unzip_file(file, fullpath):

    try: 
        os.mkdir(fullpath)
    except:
        pass

    dirname = os.path.dirname(fullpath)

    zfobj = zipfile.ZipFile(file)
    for name in zfobj.namelist():
        if name.endswith('/'):
            try: # Don't try to create a directory if exists
                os.mkdir(os.path.join(dirname, name))
            except:
                pass
        else:
            outfile = open(os.path.join(dirname, name), 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()
    
    # install_module(module_name)

def install_module(module_name):
    # TODO: dirty as hell
    settings.INSTALLED_APPS += (module_name, )
    apps.app_configs = OrderedDict()
    apps.apps_ready = apps.models_ready = apps.loading = apps.ready = False
    apps.clear_cache()
    apps.populate(settings.INSTALLED_APPS)
    management.call_command('makemigrations', module_name, interactive=False)
    #TODO: not applying
    management.call_command('migrate', module_name, interactive=False)
    
    



    
    

