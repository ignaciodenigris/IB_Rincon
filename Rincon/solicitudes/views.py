from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from herramientas.models import Proyecto
from perfil.models import Preferencias

from .forms import SolicitudServicioForm
from .models import SolicitudServicio


@login_required
def crear_solicitud(request, proyecto_id):
    proyecto = get_object_or_404(
        Proyecto,
        id=proyecto_id
    )

    # Los administradores/proveedores no solicitan servicios.
    if request.user.is_staff:
        messages.error(
            request,
            "Las cuentas de proveedor no pueden solicitar servicios."
        )
        return redirect(
            "detalle_proyecto",
            id=proyecto.id
        )

    # Evita crear varias solicitudes activas para el mismo proyecto.
    solicitud_activa = SolicitudServicio.objects.filter(
        cliente=request.user,
        proyecto=proyecto,
        estado__in=[
            "pendiente",
            "aceptada_proveedor",
            "confirmada",
            "en_proceso",
        ]
    ).first()

    if solicitud_activa:
        messages.info(
            request,
            "Ya tenés una solicitud activa para este proyecto."
        )
        return redirect(
            "detalle_solicitud",
            solicitud_id=solicitud_activa.id
        )

    preferencias = Preferencias.objects.filter(
        usuario=request.user
    ).first()

    if request.method == "POST":
        form = SolicitudServicioForm(request.POST)

        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.cliente = request.user
            solicitud.proyecto = proyecto
            solicitud.estado = "pendiente"
            solicitud.save()

            messages.success(
                request,
                "Tu solicitud fue enviada correctamente."
            )

            return redirect(
                "detalle_solicitud",
                solicitud_id=solicitud.id
            )

    else:
        datos_iniciales = {}

        if preferencias and preferencias.presupuesto:
            datos_iniciales["presupuesto_cliente"] = (
                preferencias.presupuesto
            )

        form = SolicitudServicioForm(
            initial=datos_iniciales
        )

    return render(
        request,
        "solicitudes/crear_solicitud.html",
        {
            "form": form,
            "proyecto": proyecto,
            "preferencias": preferencias,
        }
    )


@login_required
def detalle_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(
        SolicitudServicio,
        id=solicitud_id
    )

    # El cliente dueño o un administrador pueden verla.
    if (
        solicitud.cliente != request.user
        and not request.user.is_staff
    ):
        messages.error(
            request,
            "No tenés permiso para ver esta solicitud."
        )
        return redirect("perfil")

    return render(
        request,
        "solicitudes/detalle_solicitud.html",
        {
            "solicitud": solicitud
        }
    )