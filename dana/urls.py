from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)),
    path('', include('productos.urls')),
    path('clientes/', include('clientes.urls')),
    path('carrito/', include('carrito.urls')),
    path('empleados/', include('empleados.urls')),
    path('compras/', include('compras.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
