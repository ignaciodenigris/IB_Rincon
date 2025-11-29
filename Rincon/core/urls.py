from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('cuentas', include('cuentas.urls')),
    path('perfil/', include('perfil.urls')),  # ← Conecta tu app "website"
]