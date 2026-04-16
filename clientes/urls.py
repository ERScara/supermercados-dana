from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('soporte/', views.soporte, name='soporte'),
    path('eliminar-avatar/', views.eliminar_avatar, name='eliminar_avatar'),
    path('hacerse-premium/', views.hacerse_premium, name='hacerse_premium'),
]