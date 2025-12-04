from django.shortcuts import render, redirect
from .forms import PreferenciasForm
from .models import Preferencias

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


from herramientas.models import Proyecto  # IMPORTANTE

def perfil(request):
    preferencias = None
    recomendaciones = None  # ← AGREGADO

    if request.user.is_authenticated:
        preferencias = Preferencias.objects.filter(usuario=request.user).first()

        if preferencias:
            recomendaciones = Proyecto.objects.all()

            # FILTRO: estilo favorito
            if preferencias.estilo_favorito:
                recomendaciones = recomendaciones.filter(
                    subtitulo__icontains=preferencias.estilo_favorito
                )

            # FILTRO: categoría (ignorar may/min)
            if preferencias.ambientes_interes:
                recomendaciones = recomendaciones.filter(
                    categoria__iexact=preferencias.ambientes_interes
                )

            # FILTRO: presupuesto máximo
            if preferencias.presupuesto:
                recomendaciones = recomendaciones.filter(
                    precio__lte=preferencias.presupuesto
                )

    return render(request, "perfil/perfil.html", {
        "preferencias": preferencias,
        "recomendaciones": recomendaciones  # ← NECESARIO
    })