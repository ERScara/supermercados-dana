from django.db import models
from decimal import Decimal

class Carrito(models.Model):
    cliente = models.OneToOneField(
        'clientes.Cliente',
        on_delete=models.CASCADE,
        related_name='carrito'
    )
    creado_en= models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.cliente.usuario.username}"
    
    def total(self):
        """ Suma el precio total de todos los items. """
        return sum(item.subtotal() for item in self.items.all())
    
    def cantidad_items(self):
        """ Cantidad total de productos en el carrito. """
        return sum(item.cantidad for item in self.items.all())
    
    def vaciar(self):
        """ Elimina todos los items del carrito. """
        self.items.all().delete()

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(
        Carrito,
        on_delete=models.CASCADE,
        related_name='items'
    )
    producto = models.ForeignKey(
        'productos.Producto',
        on_delete=models.CASCADE,
        related_name='items_carrito'
    )
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    def __str__(self):
        """ representación del objeto. """
        return f"{self.cantidad}x {self.producto.nombre}"
    
    def subtotal(self):
        """ precio unitario por cantidad. """
        return self.precio_unitario * self.cantidad
    
    class Meta:
        unique_together = ('carrito', 'producto')