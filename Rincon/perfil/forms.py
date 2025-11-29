from django import forms
from .models import Preferencias

class PreferenciasForm(forms.ModelForm):
    class Meta:
        model = Preferencias
        fields = ['estilo_favorito', 'colores_preferidos', 'presupuesto', 'ambientes_interes']