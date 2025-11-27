
from django.contrib import admin
from django.urls import path
from .website import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registrer/', views.registrar_view, name='register'),
    path('login/', views.login_view, name='login'),
]
