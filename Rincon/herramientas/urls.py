from django.urls import path
from . import views

urlpatterns = [
    path('lista/', views.lista_proyectos, name='lista_proyectos'),
    path('<int:id>/', views.detalle_proyecto, name='detalle_proyecto'),
    path('crear/', views.crear_proyectos, name='crear_herramienta'),
]