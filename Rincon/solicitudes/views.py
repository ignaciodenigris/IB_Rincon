from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from herramientas.models import Proyecto
from perfil.models import Preferencias

from .forms import SolicitudServicioForm, RespuestaProveedorForm
from .models import SolicitudServicio
from solicitudes.models import SolicitudServicio
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

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

    if (
        solicitud.cliente != request.user
        and not request.user.is_staff
    ):
        messages.error(
            request,
            "No tenés permiso para ver esta solicitud."
        )
        return redirect("perfil")

    respuesta_form = None

    if request.user.is_staff:
        respuesta_form = RespuestaProveedorForm(
            instance=solicitud
        )

    return render(
        request,
        "solicitudes/detalle_solicitud.html",
        {
            "solicitud": solicitud,
            "respuesta_form": respuesta_form,
        }
    )
@staff_member_required
def solicitudes_proveedor(request):
    solicitudes = (
        SolicitudServicio.objects
        .select_related("cliente", "proyecto")
        .all()
    )

    estado = request.GET.get("estado")

    if estado:
        solicitudes = solicitudes.filter(estado=estado)

    return render(
        request,
        "solicitudes/solicitudes_proveedor.html",
        {
            "solicitudes": solicitudes,
            "estado_seleccionado": estado,
            "estados": SolicitudServicio.ESTADOS,
        }
    )

@staff_member_required
@require_POST
def aceptar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(
        SolicitudServicio,
        id=solicitud_id
    )

    if solicitud.estado != "pendiente":
        messages.error(
            request,
            "Solo se pueden aceptar solicitudes pendientes."
        )
        return redirect(
            "detalle_solicitud",
            solicitud_id=solicitud.id
        )

    form = RespuestaProveedorForm(
        request.POST,
        instance=solicitud
    )

    if form.is_valid():
        solicitud = form.save(commit=False)
        solicitud.estado = "aceptada_proveedor"
        solicitud.save()

        messages.success(
            request,
            "La solicitud fue aceptada."
        )
    else:
        messages.error(
            request,
            "No se pudo aceptar la solicitud."
        )

    return redirect(
        "detalle_solicitud",
        solicitud_id=solicitud.id
    )


@staff_member_required
@require_POST
def rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(
        SolicitudServicio,
        id=solicitud_id
    )

    if solicitud.estado != "pendiente":
        messages.error(
            request,
            "Solo se pueden rechazar solicitudes pendientes."
        )
        return redirect(
            "detalle_solicitud",
            solicitud_id=solicitud.id
        )

    form = RespuestaProveedorForm(
        request.POST,
        instance=solicitud
    )

    if form.is_valid():
        solicitud = form.save(commit=False)
        solicitud.estado = "rechazada"
        solicitud.save()

        messages.success(
            request,
            "La solicitud fue rechazada."
        )
    else:
        messages.error(
            request,
            "No se pudo rechazar la solicitud."
        )

    return redirect(
        "detalle_solicitud",
        solicitud_id=solicitud.id
    )

@login_required
@require_POST
def confirmar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(
        SolicitudServicio,
        id=solicitud_id,
        cliente=request.user
    )

    if solicitud.estado != "aceptada_proveedor":
        messages.error(
            request,
            "Esta solicitud no puede confirmarse en su estado actual."
        )
        return redirect(
            "detalle_solicitud",
            solicitud_id=solicitud.id
        )

    solicitud.estado = "confirmada"
    solicitud.save()

    messages.success(
        request,
        "El servicio fue confirmado correctamente."
    )

    return redirect(
        "detalle_solicitud",
        solicitud_id=solicitud.id
    )


@login_required
@require_POST
def cancelar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(
        SolicitudServicio,
        id=solicitud_id,
        cliente=request.user
    )

    if solicitud.estado not in [
        "pendiente",
        "aceptada_proveedor",
    ]:
        messages.error(
            request,
            "Esta solicitud ya no puede cancelarse."
        )
        return redirect(
            "detalle_solicitud",
            solicitud_id=solicitud.id
        )

    solicitud.estado = "cancelada"
    solicitud.save()

    messages.success(
        request,
        "La solicitud fue cancelada."
    )

    return redirect(
        "detalle_solicitud",
        solicitud_id=solicitud.id
    )