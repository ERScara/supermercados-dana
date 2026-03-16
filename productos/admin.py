from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display=('id', 'nombre', 'descripcion')
    search_field=('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display=('id', 'nombre', 'descripcion', 'precio', 'stock', 'categoria')
    list_filter=('categoria',)
    search_fields=('nombre', 'descripción')
    ordering=('categoria', 'nombre')