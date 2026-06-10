from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
    path('acerca_de/', views.acerca_de, name='acerca_de'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('soporte/', views.soporte, name='soporte'),
    path('eliminar-avatar/', views.eliminar_avatar, name='eliminar_avatar'),
    path('hacerse-premium/', views.hacerse_premium, name='hacerse_premium'),
    path('atencion/', views.inicio, name='inicio'),
    path('atencion/comentar/', views.crear_comentario, name='crear_comentario'),
    path('atencion/votar/<int:comentario_id>/', views.votar_comentario, name='votar_comentario'),
    path('atencion/reportar/<int:comentario_id>/', views.reportar_comentario, name='reportar_comentario'),
    path('atencion/eliminar/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
    path('atencion/comentario/<int:pk>/editar/', views.ComentarioUpdateView.as_view(), name='comentario_editar'),
    path('atencion/faq/', views.FAQListView.as_view(), name='faq_list'),
    path('atencion/faq/<int:pk>/', views.FAQDetailView.as_view(), name='faq_detail'),
]