from PIL import Image as PilImage
from django.db import models
from decimal import Decimal

class Categoria(models.Model):
    """ Categoría de los productos en venta. """
    nombre = models.CharField(max_length=100)
    descripcion=models.TextField(blank=True)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    """ Productos que pertenecen una determinada categoría. """
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos'
    )
    imagen=models.ImageField(upload_to='productos/', blank=True, null=True)

    @property
    def precio_con_descuento(self):
        """ Se aplica un precio con un descuento del 30% a los clientes Premium. """
        descuento = self.precio * Decimal('0.30')
        return (self.precio - descuento).quantize(Decimal('0.01'))
    
    def save(self, *args, **kwargs):
        """ Guarda las imágenes en un tamaño adecuado. """
        super().save(*args, **kwargs)
        if self.imagen:
            ruta = self.imagen.path
            img = PilImage.open(ruta)
            img.thumbnail((600, 400), PilImage.LANCZOS)
            img.save(ruta, optimize=True, quality=85)

    def __str__(self):
        """ Representación del objeto. """
        return self.nombre
