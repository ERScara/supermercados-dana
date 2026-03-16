from django.contrib import admin
from .models import Carrito, ItemCarrito

class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 0
    readonly_fields = ('subtotal',)

    def subtotal(self, obj):
        return f"${obj.subtotal()}"
    subtotal.short_description = 'Subtotal'

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'cantidad_items', 'total', 'actualizado_en')
    inlines = [ItemCarritoInline]