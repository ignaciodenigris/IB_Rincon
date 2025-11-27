from django.shortcuts import render

def base(request):
    return render(request, "website/base.html")

def about(request):
    return render(request, "website/about.html")

def gallery(request):
    return render(request, "website/gallery.html")

def register(request):
    return render(request, "website/register.html")