from django.contrib import admin
from django.db.models import Count
from .models import Comentario, VotoComentario, PreguntasFrecuentes

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'autor', 'fecha', 'parent', 'is_deleted', 'reportes_count')
    list_filter=('is_deleted', 'fecha')
    search_fields = ('mensaje', 'user__usuario__usernane')
    ordering = ('-fecha',)
    readonly_fields = ('likes_count', 'dislikes_count')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('votos', 'reportes').annotate(num_reportes=Count('reportes'))
    
    def likes_count(self, obj):
        return obj.votos.filter(voto='like').count()
    likes_count.short_description = 'Me gusta'

    def dislikes_count(self, obj):
        return obj.votos.filter(voto='dislike').count()
    likes_count.short_description = 'No me gusta'

    def autor(self, obj):
        if obj.user and obj.user.usuario:
            return obj.user.usuario.username
        return '[Usuario Eliminado]'
    autor.short_description = 'Autor'

    def reportes_count(self, obj):
        return obj.reportes.count()
    reportes_count.short_description = 'Reportes'
    
@admin.register(VotoComentario)
class VotoComentarioAdmin(admin.ModelAdmin):
    list_display = ('comentario', 'cliente', 'voto')
    list_filter = ('voto',)

@admin.register(PreguntasFrecuentes)
class PreguntasFrecuentesAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'orden')
    list_filter = ('orden', 'titulo')