from django.shortcuts import render, redirect, get_object_or_404
from .models import Proyecto
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProyectoForm

def lista_proyectos(request):
    proyectos = Proyecto.objects.all()

    # Filtros GET
    buscar = request.GET.get('buscar', '')
    categoria = request.GET.get('categoria', '')
    precio_max = request.GET.get('precio_max', '')

    if buscar:
        proyectos = proyectos.filter(titulo__icontains=buscar)

    if categoria and categoria != "todas":
        proyectos = proyectos.filter(categoria=categoria)

    if precio_max:
        proyectos = proyectos.filter(precio__lte=precio_max)

    return render(request, 'herramientas/lista.html', {
        'proyectos': proyectos,
    })

def detalle_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)

    es_favorito = False
    if request.user.is_authenticated:
        es_favorito = request.user in proyecto.favoritos.all()

    return render(request, "herramientas/detalle.html", {
        "proyecto": proyecto,
        "es_favorito": es_favorito
    })

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

@login_required
@user_passes_test(es_admin)
def editar_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)

    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('detalle_proyecto', id=id)
    else:
        form = ProyectoForm(instance=proyecto)

    return render(request, 'herramientas/editar_proyecto.html', {'form': form, 'proyecto': proyecto})

@login_required
@user_passes_test(es_admin)
def eliminar_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    proyecto.delete()
    return redirect('lista_proyectos')

from django.db.models import Count

@login_required
@user_passes_test(es_admin)
def proyectos_populares(request):
    if not request.user.is_staff:
        return redirect('home')

    proyectos = Proyecto.objects.annotate(
        total_favoritos=Count('favoritos')
    ).order_by('-total_favoritos')[:5]

    return render(request, 'herramientas/populares.html', {
        'proyectos': proyectos
    })

@login_required
def toggle_favorito(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)

    if request.user in proyecto.favoritos.all():
        proyecto.favoritos.remove(request.user)
    else:
        proyecto.favoritos.add(request.user)

    return redirect(request.META.get("HTTP_REFERER", "perfil"))