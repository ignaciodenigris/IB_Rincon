from django.shortcuts import render, redirect
from .forms import PreferenciasForm
from .models import Preferencias
from herramientas.models import Proyecto


def cuestionario(request):
    if request.method == 'POST':
        form = PreferenciasForm(request.POST)
        if form.is_valid():
            preferencias = form.save(commit=False)
            preferencias.usuario = request.user
            preferencias.save()
            return redirect('perfil')
    else:
        form = PreferenciasForm()

    return render(request, 'perfil/cuestionario.html', {'form': form})


def perfil(request):
    preferencias = None
    recomendaciones = None
    proyectos_guardados = None

    if request.user.is_authenticated:
        preferencias = Preferencias.objects.filter(
            usuario=request.user
        ).first()

        proyectos_guardados = Proyecto.objects.filter(
            favoritos=request.user
        )

        if preferencias:
            recomendaciones = Proyecto.objects.all()

            if preferencias.estilo_favorito:
                recomendaciones = recomendaciones.filter(
                    subtitulo__icontains=preferencias.estilo_favorito
                )

            if preferencias.ambientes_interes:
                recomendaciones = recomendaciones.filter(
                    categoria__iexact=preferencias.ambientes_interes
                )

            if preferencias.presupuesto:
                recomendaciones = recomendaciones.filter(
                    precio__lte=preferencias.presupuesto
                )

    return render(request, "perfil/perfil.html", {
        "preferencias": preferencias,
        "recomendaciones": recomendaciones,
        "proyectos_guardados": proyectos_guardados,
    })

