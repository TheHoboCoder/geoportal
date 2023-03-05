from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('modules/', views.ModuleListView.as_view()),
    path('modules/create', views.create_module),
    path('modules/create_succes/', views.on_created),
    path('modules/<str:module_name>/commands/', views.get_commands),
    path('modules/<str:module_name>/commands/<str:command_name>/', views.run_command),
    path('modules/<str:module_name>/areas/', views.AreaListView.as_view()),
    path('modules/<str:module_name>/areas/<str:area_name>/', views.LayerListView.as_view()),
    path('modules/<str:module_name>/areas/<str:area_name>/<str:layer_name>/', views.LayerContentListView.as_view()),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
