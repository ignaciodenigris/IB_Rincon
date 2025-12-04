from django.db import models

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

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo