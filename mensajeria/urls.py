from django.urls import path
from . import views

urlpatterns = [
    path('', views.mensajeria, name='mensajeria'),
    path('<int:conversacion_id>/', views.mensajeria, name='mensajeria'),
]