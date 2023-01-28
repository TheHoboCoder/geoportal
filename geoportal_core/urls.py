from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('modules/', views.ModuleListView.as_view()),
    path('modules/create', views.create_module),
    path('modules/create_succes/', views.on_created),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
