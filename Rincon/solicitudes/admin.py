from django.contrib import admin
from .models import SolicitudServicio
@admin.register(SolicitudServicio)
class SolicitudServicioAdmin(admin.ModelAdmin):
    list_display = (
        "cliente",
        "proyecto",
        "presupuesto_cliente",
        "estado",
        "fecha_solicitud",
    )

    list_filter = (
        "estado",
        "fecha_solicitud",
    )

    search_fields = (
        "cliente__username",
        "proyecto__titulo",
    )