from django.urls import path
from . import views

app_name = 'empleados'

urlpatterns = [
    path('', views.lista_empleados, name='lista_empleados'),
    path('nuevo/', views.registro_empleado, name='registro_empleados'),
]