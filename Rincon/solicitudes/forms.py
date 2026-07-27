from django import forms
from .models import SolicitudServicio


class SolicitudServicioForm(forms.ModelForm):
    class Meta:
        model = SolicitudServicio

        fields = [
            "presupuesto_cliente",
            "mensaje",
            "fecha_estimada",
        ]

        labels = {
            "presupuesto_cliente": "Presupuesto disponible",
            "mensaje": "Contanos qué servicio necesitás",
            "fecha_estimada": "Fecha aproximada",
        }

        widgets = {
            "presupuesto_cliente": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "step": "0.01",
                    "placeholder": "Ejemplo: 500000",
                }
            ),
            "mensaje": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": (
                        "Describí el ambiente, los cambios que querés "
                        "realizar y cualquier detalle importante."
                    ),
                }
            ),
            "fecha_estimada": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }

    def clean_presupuesto_cliente(self):
        presupuesto = self.cleaned_data["presupuesto_cliente"]

        if presupuesto <= 0:
            raise forms.ValidationError(
                "El presupuesto debe ser mayor que cero."
            )

        return presupuesto

class RespuestaProveedorForm(forms.ModelForm):
    class Meta:
        model = SolicitudServicio
        fields = [
            "respuesta_proveedor",
        ]

        labels = {
            "respuesta_proveedor": "Respuesta al cliente",
        }

        widgets = {
            "respuesta_proveedor": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": (
                        "Explicá condiciones, disponibilidad o "
                        "cualquier información relevante."
                    ),
                }
            ),
        }