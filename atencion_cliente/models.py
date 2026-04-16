from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class PreguntasFrecuentes(models.Model):
    titulo = models.CharField(max_length=120)
    respuesta = models.TextField()
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'titulo']
    
    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    user = models.ForeignKey(
        'clientes.Cliente',
        on_delete = models.CASCADE,
        related_name = 'comentarios'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='respuestas'
    )
    puntuacion = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    titulo = models.CharField(max_length=100)
    mensaje = models.TextField(max_length=3000)
    fecha = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    reportes = models.ManyToManyField(
        'clientes.Cliente',
        blank=True,
        related_name='reported_comments'
    )

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.user} - {self.titulo} - {self.puntuacion} ⭐"
    
    @property
    def estrellas(self):
        """ Devuelve las estrellas como una cadena de caracteres visual. """
        return '⭐' * self.puntuacion + '☆' * (5 - self.puntuacion)

    @property
    def reported(self):
        return self.reportes.exists()
    
class VotoComentario(models.Model):
    """ Me gusta / No me gusta en un comentario """
    VOTO_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike')
    ]
    comentario = models.ForeignKey(
        Comentario,
        on_delete=models.CASCADE,
        related_name = 'votos'
    )
    cliente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.CASCADE,
        related_name='voto_comentario'
    )
    voto = models.CharField(max_length=10, choices=VOTO_CHOICES)
    
    def __str__(self):
        return f"{self.cliente.usuario.username} -> {self.voto} en el comentario #{self.comentario.id}"
