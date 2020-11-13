from .views import index
from django.urls import path


urlpatterns = [
    path(r'', index, name='index'),
]




