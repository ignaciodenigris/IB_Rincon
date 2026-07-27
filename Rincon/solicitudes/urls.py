from django.urls import include, path
from django.contrib import admin
from . import views


urlpatterns = [
    path("crear/<int:proyecto_id>/",views.crear_solicitud,name="crear_solicitud" ),
    path("<int:solicitud_id>/",views.detalle_solicitud,name="detalle_solicitud"),
    path("proveedor/",views.solicitudes_proveedor, name="solicitudes_proveedor"),
    path("<int:solicitud_id>/confirmar/",views.confirmar_solicitud,name="confirmar_solicitud"),
    path("<int:solicitud_id>/cancelar/",views.cancelar_solicitud,name="cancelar_solicitud"), 
]

