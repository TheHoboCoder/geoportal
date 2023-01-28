from django.urls import path
from .base.base_urls import base_urls

urlpatterns = [
   # custom_urls
] 

urlpatterns.extend(base_urls)
