from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('sobre-nosotros/', views.about, name="about"),
    path('galeria/', views.gallery, name="gallery"),
    path('registrarse/', views.register, name="register"),
]