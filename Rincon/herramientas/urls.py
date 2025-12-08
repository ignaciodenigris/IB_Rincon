from django.urls import path
from . import views

urlpatterns = [
    path('lista/', views.lista_proyectos, name='lista_proyectos'),
    path('<int:id>/', views.detalle_proyecto, name='detalle_proyecto'),
    path('crear/', views.crear_proyectos, name='crear_herramienta'),
    path('editar/<int:id>/', views.editar_proyecto, name='editar_proyecto'),
    path('eliminar/<int:id>/', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('detalle/<int:id>/', views.detalle_proyecto, name='detalle_proyecto'),
]