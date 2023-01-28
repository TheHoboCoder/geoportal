from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import ModuleListSerializer
from .models import GISModule
from .forms import GISModuleForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

class ModuleListView(ListAPIView):
    serializer_class = ModuleListSerializer
    queryset = GISModule.objects.all()

def create_module(request):
    # TODO: redirect to login
    if not request.user.is_authenticated:
        return HttpResponse('must authorize', status=403)
    if request.method == 'POST':
        form = GISModuleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(owner=request.user)
            return HttpResponseRedirect('create_succes/')

    else:
        form = GISModuleForm()

    return render(request, 'geoportal_core/add_module.html', {'form': form})

def on_created(request):
    return HttpResponse('<b>Uploaded</b>')
