from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('productos/', views.lista_productos, name='lista'),
    path('productos/<int:pk>/', views.detalle_producto, name='detalle'),
    path('buscar/', views.buscar, name='buscar'),
]