from django.urls import path
from .views import cuestionario, perfil 
urlpatterns = [
    path('cuestionario/', cuestionario, name='cuestionario'),
    path("", perfil, name="perfil"),
]