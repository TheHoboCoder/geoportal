from django import forms
from .models import GISModule
import zipfile, os
from django.conf import settings

class GISModuleForm(forms.ModelForm):
    module_file = forms.FileField()

    class Meta:
        model = GISModule
        exclude = ['owner']

    def save(self, owner, commit: bool = True):
        module_file = self.cleaned_data['module_file']
        del self.cleaned_data['module_file']
        save_file(module_file, self.cleaned_data['name'])
        model = super().save(commit=False)
        if commit:
            model.owner = owner
            model.save()
        return model

def save_file(file, module_name):
    # with open(f'zipped/{module_name}.zip', 'wb+') as destination:
    #     for chunk in file.chunks():
    #         destination.write(chunk)

    fullpath = os.path.join(settings.MEDIA_ROOT, f"modules\\{module_name}")

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

    
    


