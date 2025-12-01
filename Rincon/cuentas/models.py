from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    imagen_perfil = models.ImageField(
        upload_to='perfiles/',
        default='default.jpg',
        blank=True,
        null=True
    )