from django.urls import path
from . import views

app_name = 'atencion_cliente'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('votar/<int:comentario_id>/', views.votar, name='votar'),
    path('comentar/', views.crear_comentario, name='crear_comentario'),
    path('reportar/<int:comentario_id>/', views.reportar, name='reportar'),
    path('eliminar/<int:comentario_id>/', views.eliminar,  name='eliminar'),
]