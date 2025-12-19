from django.shortcuts import render, redirect

def base(request):
    return render(request, "website/base.html")

def about(request):
    return render(request, "website/about.html")

def gallery(request):
    return render(request, "website/gallery.html")

def register(request):
    # Redirige a la vista de registro de la app `cuentas` para asegurar
    # que el formulario se pase correctamente a la plantilla.
    return redirect('cuentas:registro')