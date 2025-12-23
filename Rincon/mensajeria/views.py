from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversacion, Mensaje
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def mensajeria(request, conversacion_id=None):
    user = request.user

    # Si es admin, ve todas las conversaciones
    if user.is_staff:
        conversaciones = Conversacion.objects.all().order_by('-actualizado')
    else:
        conversaciones = Conversacion.objects.filter(cliente=user)

    # Si el cliente no tiene conversación, se crea una con el primer admin
    if not user.is_staff and not conversaciones.exists():
        admin = User.objects.filter(is_staff=True).first()
        if admin:
            Conversacion.objects.create(cliente=user, admin=admin)
        conversaciones = Conversacion.objects.filter(cliente=user)

    # Conversación activa en el panel
    conversacion_activa = None
    if conversacion_id:
        conversacion_activa = get_object_or_404(Conversacion, id=conversacion_id)

    # Envío de mensaje
    if request.method == "POST":
        contenido = request.POST.get("mensaje")
        if conversacion_activa and contenido.strip():
            Mensaje.objects.create(
                conversacion=conversacion_activa,
                remitente=user,
                contenido=contenido
            )
            conversacion_activa.save()
            return redirect('mensajeria', conversacion_activa.id)

    return render(request, 'mensajeria/chat.html', {
        "conversaciones": conversaciones,
        "conversacion_activa": conversacion_activa
    })