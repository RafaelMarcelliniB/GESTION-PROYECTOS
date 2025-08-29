from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('estudiantes/', views.lista_estudiantes, name='estudiantes'),
    path('reporte/', views.reporte_rendimiento, name='reporte'),
    path('recomendaciones/', views.recomendaciones, name='recomendaciones'),
]
