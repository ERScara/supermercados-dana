from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.db import models

class Cliente(models.Model):
    """ Clientes del supermercado. """
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    edad=models.PositiveIntegerField(default=0)
    es_cliente_premium=models.BooleanField(default=False)
    saldo_a_favor=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    preferencias = models.ManyToManyField(
        'productos.Categoria',
        blank=True,
        related_name='clientes_interesados'
    )
    avatar = models.ImageField(
        upload_to='avatares/',
        blank=True,
        null=True,
        default=None
    )

    def __str__(self):
        """ Representación del cliente y su estado de subscripción. """
        estado = "Premium" if self.es_cliente_premium else "Regular"
        return f"{self.usuario.get_full_name()} ({estado})"

    def hacer_cliente_premium(self):
        """ Subscribe al cliente a Premium y le otorga un bono de bienvenida. 
            \nEl cliente sube de categoría y obtiene beneficios. 
        """
        self.refresh_from_db()
        if not self.es_cliente_premium:
            self.es_cliente_premium = True
            self.saldo_a_favor += Decimal('1000.00')
            self.save()
            return f"¡Felicidades, {self.usuario.first_name}! Ya eres cliente Premium."
        return f"{self.usuario.first_name}, ya eres cliente Premium"
    
    @classmethod
    def numero_clientes(cls):
        """ Cuenta la cantidad de clientes que hay en el sitio. """
        return cls.objects.count()
    
    @staticmethod
    def validar_email(email):
        """
        Método para validar el correo electrónico del cliente.
        \nBusca la existencia de '@' y '.' en los correos electrónicos.
        """
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False
        
    def get_avatar_url(self):
        """ Devuelve avatar del cliente o una imagen por defecto. """
        if self.avatar:
            return self.avatar.url
        return '/static/img/avatar_default.svg'

class SupportTicket(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    reason = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Ticket de {self.username} - {self.created_at.strftime('%d/%m/%Y')}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Ticket de soporte'
        verbose_name_plural = 'Tickets de soporte'