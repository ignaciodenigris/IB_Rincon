from django.db import models
from django.conf import settings
from herramientas.models import Proyecto
# Create your models here.

class SolicitudServicio(models.Model):

    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("aceptada_proveedor", "Aceptada por el proveedor"),
        ("confirmada", "Confirmada por el cliente"),
        ("rechazada", "Rechazada"),
        ("cancelada", "Cancelada"),
        ("en_proceso", "En proceso"),
        ("finalizada", "Finalizada"),
    ]

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="solicitudes_servicio"
    )

    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name="solicitudes"
    )

    presupuesto_cliente = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    mensaje = models.TextField(
        blank=True
    )

    respuesta_proveedor = models.TextField(
        blank=True
    )

    fecha_estimada = models.DateField(
        null=True,
        blank=True
    )

    estado = models.CharField(
        max_length=30,
        choices=ESTADOS,
        default="pendiente"
    )

    fecha_solicitud = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-fecha_solicitud"]

    def __str__(self):
        return f"{self.cliente.username} - {self.proyecto.titulo}"