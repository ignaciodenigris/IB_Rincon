from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistroForm
from django.contrib import messages

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('cuestionario')
    else:
        form = RegistroForm()

    return render(request, "cuentas/registro.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("base")  # Cambia "home" por el nombre real de tu home
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "cuentas/login.html")