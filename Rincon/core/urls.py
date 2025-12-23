from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('cuentas/', include('cuentas.urls')),
    path('perfil/', include('perfil.urls')), 
    path('herramientas/', include('herramientas.urls')),
    path('mensajeria/', include('mensajeria.urls')),
     path('logout/', LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)