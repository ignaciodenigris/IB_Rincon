from django.shortcuts import render, redirect, get_object_or_404
from .models import Proyecto, Resena
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProyectoForm, ResenaForm
from django.db.models import Count, Avg

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
    resena_usuario = None

    if request.user.is_authenticated:
        es_favorito = request.user in proyecto.favoritos.all()
        resena_usuario = Resena.objects.filter(
            proyecto=proyecto,
            usuario=request.user
        ).first()

    resenas = proyecto.resenas.select_related("usuario").all()

    estadisticas = resenas.aggregate(
        promedio=Avg("puntuacion"),
        cantidad=Count("id")
    )

    return render(request, "herramientas/detalle.html", {
        "proyecto": proyecto,
        "es_favorito": es_favorito,
        "resenas": resenas,
        "resena_usuario": resena_usuario,
        "promedio_resenas": estadisticas["promedio"],
        "cantidad_resenas": estadisticas["cantidad"],
    })

def es_admin(user):
    return user.is_staff

@login_required
@user_passes_test(es_admin)
def crear_proyectos(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.creador = request.user 
            proyecto.save()                       
            return redirect('lista_proyectos')
    else:
        form = ProyectoForm()

    return render(request, 'herramientas/crear_proyecto.html', {
        'form': form
    })

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

@login_required
def guardar_resena(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)

    resena, creada = Resena.objects.get_or_create(
        proyecto=proyecto,
        usuario=request.user,
        defaults={
            "puntuacion": 5,
            "comentario": ""
        }
    )

    if request.method == "POST":
        form = ResenaForm(request.POST, instance=resena)

        if form.is_valid():
            form.save()
            return redirect("detalle_proyecto", id=proyecto.id)
    else:
        form = ResenaForm(instance=resena)

    return render(request, "herramientas/resena_form.html", {
        "form": form,
        "proyecto": proyecto,
        "creada": creada,
    })


@login_required
def eliminar_resena(request, id):
    resena = get_object_or_404(
        Resena,
        id=id,
        usuario=request.user
    )

    proyecto_id = resena.proyecto.id

    if request.method == "POST":
        resena.delete()

    return redirect("detalle_proyecto", id=proyecto_id)