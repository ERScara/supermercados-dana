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

    def ahorro(self):
        return sum((item.subtotal() - item.precio_unitario ) for item in self.items.all())
    
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
    precio_original = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null= True
    )
    def __str__(self):
        """ representación del objeto. """
        return f"{self.cantidad} x {self.producto.nombre}"
    
    @property
    def tiene_descuento(self):
        """ Devuelve verdadero si el item tiene descuento. """
        if self.precio_original and self.precio_unitario:
            return self.precio_unitario < self.precio_original
        return False

    @property
    def ahorro(self):
        """ Indica cuánto ahorró el cliente por descuento """
        if self.tiene_descuento:
            return (self.precio_original - self.precio_unitario) * self.cantidad
        return Decimal('0.00')
    
    @property
    def ahorro_total(self):
        return sum(item.ahorro for item in self.items.all())
    
    def subtotal(self):
        """ precio unitario por cantidad. """
        if self.precio_unitario is None:
            return Decimal('0.00')
        return self.precio_unitario * self.cantidad
    
    class Meta:
        unique_together = ('carrito', 'producto')