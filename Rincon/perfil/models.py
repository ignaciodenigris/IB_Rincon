from django.db import models
from django.conf import settings

class Preferencias(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    estilo_favorito = models.CharField(
        max_length=50,
        choices=[
            ('moderno', 'Moderno'),
            ('minimalista', 'Minimalista'),
            ('rustico', 'Rústico'),
            ('clasico', 'Clásico'),
        ]
    )
    colores_preferidos = models.CharField(max_length=200)
    presupuesto = models.IntegerField()
    ambientes_interes = models.CharField(max_length=200)

    def __str__(self):
        return f"Preferencias de {self.usuario.username}"