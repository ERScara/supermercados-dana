from django.db import models
from django.contrib.auth.models import User

class Empleado(models.Model):
    """ Empleados del supermercado. """

    SECTOR_CHOICES = [
        ('Atención al cliente', 'Atención al cliente'),
        ('Caja', 'Caja'),
        ('Reposición', 'Reposición'),
        ('Seguridad', 'Seguridad'),
        ('Limpieza', 'Limpieza'),
        ('Administración', 'Administración')
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empleado')
    legajo = models.CharField(max_length=20, unique=True)
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES, default='atencion')
    fecha_alta = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(
        upload_to='avatares_empleados/',
        blank=True,
        null=True,
    )
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario.get_full_name() or self.usuario.username} - {self.get_sector_display()}"
    
    def get_avatar_url(self):
        """ Devuelve avatar del empleado o una imagen por defecto. """
        if self.avatar:
            return self.avatar.url
        return '/static/img/avatar_default.svg'
    
    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['sector', 'usuario__username']