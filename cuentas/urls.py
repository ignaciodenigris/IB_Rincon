from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = "cuentas"
urlpatterns = [
    path("registro/", views.registro, name="registro"),
    path("login/", views.login_view, name="login"),
    path("actualizar-foto/", views.actualizar_foto, name="actualizar_foto"),
]