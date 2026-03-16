from django.urls import path
from . import views

app_name = 'compras'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('confirmar/', views.confirmar, name='confirmar'),
    path('confirmar/<int:compra_id>/', views.confirmar, name='confirmar')
]