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


    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        
        for instance in instances:
            if isinstance(instance, ItemCarrito):
                if not instance.precio_unitario:
                    instance.precio_unitario = instance.producto.precio
                if not instance.precio_original:
                    instance.precio_original = instance.producto.precio
            instance.save()
        formset.save_m2m()

    def get_queryset(self,request):
        return super().get_queryset(request).prefetch_related('items__producto')    