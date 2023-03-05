from django.contrib import admin
from . import models, forms

@admin.register(models.GISModule)
class GISModuleAdmin(admin.ModelAdmin):
    form = forms.EditGISModuleForm

    def get_queryset(self, request):
        if request.user.is_superuser:
            return models.GISModule.objects.all()
        return models.GISModule.objects.filter(owner=request.user)

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = forms.CreateGISModuleForm
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        forms.remove_module_dir(obj.name)
        super().delete_model(request, obj)

    
admin.site.register(models.Layer)
admin.site.register(models.Area)
admin.site.register(models.VectorFeature)




