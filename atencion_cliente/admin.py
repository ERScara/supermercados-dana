from django.contrib import admin
from django.db.models import Count
from .models import Comentario, VotoComentario, PreguntasFrecuentes

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'autor', 'fecha', 'parent', 'is_deleted', 'reportes_count')
    list_filter=('is_deleted', 'fecha')
    search_fields = ('mensaje', 'user__usuario__usernane')
    ordering = ('-fecha',)

    def autor(self, obj):
        if obj.user and obj.user.usuario:
            return obj.user.usuario.username
        return '[Usuario Eliminado]'
    autor.short_description = 'Autor'

    def reportes_count(self, obj):
        return obj.reportes.count()
    reportes_count.short_description = 'Reportes'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('reportes').annotate(num_reportes=Count('reportes'))