from django.contrib import admin
from django.contrib.auth.models import User
from .models import Cliente, SupportTicket

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display=('usuario', 'edad', 'es_cliente_premium', 'saldo_a_favor', 'mostrar_preferencias')
    list_filter=('es_cliente_premium',)
    search_fields=('usuario__username', 'usuario__email')
    ordering=('id', 'edad',)

    def mostrar_preferencias(self, obj):
        return ", ".join([cat.nombre for cat in obj.preferencias.all()])
    
    mostrar_preferencias.short_description = "Preferencias"

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_at', 'reason')
    list_filter = ('resolved', 'created_at')
    search_fields = ('username', 'email', 'reason')
    ordering= ('-created_at',)

    actions= ['eliminar_usuario_asociado']

    @admin.action(description='Eliminar usuario de este ticket')
    def eliminar_usuario_asociado(self, request, queryset):
        for ticket in queryset:
            try:
                user= User.objects.get(username=ticket.username)
                user.delete()
                ticket.resolved = True
                ticket.save()
                self.message_user(
                    request,
                    f"Usuario '{ticket.username}' eliminado correctamente."
                )
            except User.DoesNotExist:
                self.message_user(
                    request,
                    f"El usuario '{ticket.username}' ya no existe.",
                )
