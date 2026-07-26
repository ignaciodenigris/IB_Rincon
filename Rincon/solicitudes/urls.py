from django.urls import include, path
from django.contrib import admin
from . import views


urlpatterns = [
    path(
        "crear/<int:proyecto_id>/",
        views.crear_solicitud,
        name="crear_solicitud"
    ),
    path(
        "<int:solicitud_id>/",
        views.detalle_solicitud,
        name="detalle_solicitud"
    ),
]

