from django.urls import path

from . import views


urlpatterns = [
    path(
        "crear/<int:proyecto_id>/",
        views.crear_solicitud,
        name="crear_solicitud",
    ),
    path(
        "proveedor/",
        views.solicitudes_proveedor,
        name="solicitudes_proveedor",
    ),
    path(
        "cliente/<int:cliente_id>/",
        views.detalle_cliente,
        name="detalle_cliente",
    ),
    path(
        "<int:solicitud_id>/",
        views.detalle_solicitud,
        name="detalle_solicitud",
    ),
    path(
        "<int:solicitud_id>/aceptar/",
        views.aceptar_solicitud,
        name="aceptar_solicitud",
    ),
    path(
        "<int:solicitud_id>/rechazar/",
        views.rechazar_solicitud,
        name="rechazar_solicitud",
    ),
    path(
        "<int:solicitud_id>/confirmar/",
        views.confirmar_solicitud,
        name="confirmar_solicitud",
    ),
    path(
        "<int:solicitud_id>/cancelar/",
        views.cancelar_solicitud,
        name="cancelar_solicitud",
    ),
    path(
        "<int:solicitud_id>/iniciar/",
        views.iniciar_servicio,
        name="iniciar_servicio",
    ),
    path(
        "<int:solicitud_id>/finalizar/",
        views.finalizar_servicio,
        name="finalizar_servicio",
    ),
]
