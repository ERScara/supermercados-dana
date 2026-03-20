from django.db import models
from decimal import Decimal

class Compra(models.Model):

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada',  'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]

    cliente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.PROTECT,
        related_name='historial_compras'
    )
    fecha             = models.DateTimeField(auto_now_add=True)
    total             = models.DecimalField(
                            max_digits=10,
                            decimal_places=2,
                            default=Decimal('0.00')
                        )
    estado            = models.CharField(
                            max_length=20,
                            choices=ESTADO_CHOICES,
                            default='pendiente'
                        )
    ultimos_4_digitos = models.CharField(max_length=4, blank=True, default='')

    @property
    def ahorro_total(self):
        total_ahorro = sum(item.ahorro for item in self.items.all())
        return total_ahorro if total_ahorro > 0 else Decimal('0.00')

    def __str__(self):
        return f"Compra #{self.id} — {self.cliente.usuario.username} — ${self.total}"

    class Meta:
        ordering = ['-fecha']

class ItemCompra(models.Model):
    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name='items'
    )
    producto = models.ForeignKey(
        'productos.Producto',
        on_delete=models.PROTECT,
        related_name='items_compra'
    )
    cantidad        = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_original = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

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
        return 0

    def get_ahorro_display(self):
        return self.ahorro
    
    def get_precio_original_display(self):
        return self.precio_original or '-'

    def subtotal(self):
        return self.precio_unitario * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"