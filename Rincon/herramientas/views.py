from django.shortcuts import render, redirect, get_object_or_404
from .models import Proyecto
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProyectoForm

def lista_proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'herramientas/lista.html', {'proyectos': proyectos})

def detalle_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    return render(request, 'herramientas/detalle.html', {'proyecto': proyecto})

def es_admin(user):
    return user.is_staff

@login_required
@user_passes_test(es_admin)
def crear_proyectos(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_proyectos')
    else:
        form = ProyectoForm()

    return render(request, 'herramientas/crear_proyecto.html', {'form': form})