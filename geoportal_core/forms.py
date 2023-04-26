from django import forms
from .models import GISModule, Layer, VectorFeature, RasterFeature
from django.core.exceptions import ValidationError
from . import module_filesystem as utils
from zipfile import BadZipfile, LargeZipFile

class EditGISModuleForm(forms.ModelForm):
    class Meta:
        model = GISModule
        exclude = ['owner']

class CreateGISModuleForm(forms.ModelForm):
    module_file = forms.FileField()

    def clean_module_file(self):
        if not self.cleaned_data['module_file'].name.endswith('.zip'):
            raise ValidationError('Only .zip files allowed')
        return self.cleaned_data['module_file']
    
    def clean(self):
        cleaned_data = super().clean()

        try:
            utils.unzip_file(cleaned_data["module_file"], cleaned_data["name"])
        except BadZipfile as zip_error:
            utils.remove_module_dir(cleaned_data["name"])
            raise ValidationError(f"Невозможно открыть архив. Проверьте, что файл не поврежден. ({zip_error})")
        except OSError as os_error:
            utils.remove_module_dir(cleaned_data["name"])
            raise ValidationError(f"Ошибка при создании файлов: {os_error}")
        except Exception as err:
            utils.remove_module_dir(cleaned_data["name"])
            raise ValidationError(f"Неизвестная ошибка при распаковке архива: {err}")
        
        try:
            utils.try_import(cleaned_data["name"])
        except ModuleNotFoundError as not_found:
            utils.remove_module_dir(cleaned_data["name"])
            raise ValidationError(f'Невозможно открыть файл конфигурации module_config.py: {not_found}')
        except AttributeError as att:
            utils.remove_module_dir(cleaned_data["name"])
            raise ValidationError(f'Ошибка при чтении COMMANDS and SCHEMA: {att}')
        except Exception as err:
            utils.remove_module_dir(cleaned_data["name"])
            raise ValidationError(f"Неизвестная ошибка при импортировании конфигурации: {err}")

    class Meta:
        model = GISModule
        exclude = ['owner']

    def save(self, commit: bool = True):
        del self.cleaned_data['module_file']
        model = super().save(commit=False)
        return model
    
class LayerAdminForm(forms.ModelForm):

    def clean_layer_type(self):
        # попытка изменить тип слоя с привязанными к нему объектами
        if self.instance is not None and self.instance.pk is not None:
            cls = RasterFeature if self.cleaned_data["layer_type"] == 'V' else VectorFeature
            if cls.objects.filter(layer=self.instance.pk).count() > 0:
                raise ValidationError("Вы пытаетесь изменить тип слоя, но он содержит объекты."+
                                      "Удалите их или переместите на другой слой.")
        return self.cleaned_data["layer_type"]
    
    def clean(self):
        super().clean()
        if self.cleaned_data["area"] is not None and \
           self.cleaned_data["module"] != self.cleaned_data["area"].module:
            raise ValidationError("Область должна принадлежать указанному модулю")

    class Meta:
        model = Layer
        fields = '__all__'

class VectorFeatureAdminForm(forms.ModelForm):
     
    def clean(self):
        super().clean()
        if self.cleaned_data["area"].module != self.cleaned_data["layer"].module:
            raise ValidationError("Область и слой должны находится в одном модуле")
        
    class Meta:
        model = VectorFeature
        fields = '__all__'


    
    



    
    


