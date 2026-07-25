from django import forms
from .models import Proyecto
from .models import Resena

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['titulo', 'subtitulo', 'descripcion', 'precio', 'imagen', 'categoria']

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }
class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ["puntuacion", "comentario"]

        widgets = {
            "puntuacion": forms.Select(
                choices=[(1, "★☆☆☆☆"),
                         (2, "★★☆☆☆"),
                         (3, "★★★☆☆"),
                         (4, "★★★★☆"),
                         (5, "★★★★★")],
                attrs={"class": "form-control"}
            ),
            "comentario": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Escribí tu opinión sobre este proyecto..."
                }
            ),
        }