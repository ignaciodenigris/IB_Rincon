from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from herramientas.models import Proyecto
from solicitudes.models import SolicitudServicio

from .forms import PreferenciasForm
from .models import Preferencias


@login_required
def cuestionario(request):
    preferencias = Preferencias.objects.filter(usuario=request.user).first()

    if request.method == "POST":
        form = PreferenciasForm(request.POST, instance=preferencias)

        if form.is_valid():
            nuevas_preferencias = form.save(commit=False)
            nuevas_preferencias.usuario = request.user
            nuevas_preferencias.save()
            return redirect("perfil")
    else:
        form = PreferenciasForm(instance=preferencias)

    return render(request, "perfil/cuestionario.html", {"form": form})


@login_required
def perfil(request):
    preferencias = Preferencias.objects.filter(usuario=request.user).first()

    proyectos_guardados = Proyecto.objects.filter(favoritos=request.user)

    solicitudes_cliente = SolicitudServicio.objects.filter(
        cliente=request.user
    ).select_related("proyecto")

    recomendaciones = []

    if preferencias:
        proyectos = Proyecto.objects.exclude(favoritos=request.user)

        colores_usuario = [
            color.strip().lower()
            for color in preferencias.colores_preferidos.split(",")
            if color.strip()
        ]

        ambientes_usuario = [
            ambiente.strip().lower()
            for ambiente in preferencias.ambientes_interes.split(",")
            if ambiente.strip()
        ]

        for proyecto in proyectos:
            puntaje = 0
            motivos = []

            subtitulo = (proyecto.subtitulo or "").lower()
            descripcion = (proyecto.descripcion or "").lower()
            categoria = (proyecto.categoria or "").lower()
            texto_proyecto = f"{subtitulo} {descripcion} {categoria}"

            if (
                preferencias.estilo_favorito
                and preferencias.estilo_favorito.lower() in texto_proyecto
            ):
                puntaje += 3
                motivos.append("Estilo favorito")

            if categoria in ambientes_usuario:
                puntaje += 4
                motivos.append("Ambiente de interés")

            if any(color in texto_proyecto for color in colores_usuario):
                puntaje += 2
                motivos.append("Colores preferidos")

            if (
                preferencias.presupuesto
                and proyecto.precio <= preferencias.presupuesto
            ):
                puntaje += 3
                motivos.append("Dentro de tu presupuesto")

            # Solo se muestran coincidencias relevantes.
            if puntaje >= 3:
                recomendaciones.append({
                    "proyecto": proyecto,
                    "puntaje": puntaje,
                    "motivos": motivos,
                })

        recomendaciones.sort(
            key=lambda recomendacion: recomendacion["puntaje"],
            reverse=True,
        )

    return render(request, "perfil/perfil.html", {
        "preferencias": preferencias,
        "recomendaciones": recomendaciones,
        "proyectos_guardados": proyectos_guardados,
        "solicitudes_cliente": solicitudes_cliente,
    })
