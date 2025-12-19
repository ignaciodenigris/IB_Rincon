from django.db import models
from django.conf import settings

CATEGORIAS = [
    ('living', 'Living'),
    ('cocina', 'Cocina'),
    ('banio', 'Baño'),
    ('dormitorio', 'Dormitorio'),
    ('oficina', 'Oficina'),
    ('exterior', 'Exterior'),
]

class Proyecto(models.Model):
    titulo = models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=150, blank=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='proyectos/')
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='living')


    creador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="proyectos_creados"
    )


    favoritos = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="proyectos_favoritos",
        blank=True    )

    def __str__(self):
        return self.titulo
    
