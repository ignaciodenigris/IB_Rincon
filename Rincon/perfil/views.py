from django.shortcuts import render, redirect
from .forms import PreferenciasForm, Preferencias

def cuestionario(request):
    if request.method == 'POST':
        form = PreferenciasForm(request.POST)
        if form.is_valid():
            preferencias = form.save(commit=False)
            preferencias.usuario = request.user
            preferencias.save()
            return redirect('perfil')  # vista del perfil luego
    else:
        form = PreferenciasForm()

    return render(request, 'perfil/cuestionario.html', {'form': form})

def perfil(request):
    preferencias = None
    if request.user.is_authenticated:
        preferencias = Preferencias.objects.filter(usuario=request.user).first()
        
    return render(request, "perfil/perfil.html", {
        "preferencias": preferencias
    })