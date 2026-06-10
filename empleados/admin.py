from django.contrib import admin
from .models import Empleado
@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'legajo', 'sector', 'fecha_alta', 'activo')
    list_filter = ('sector', 'activo')
    search_fields = ('usuario__username', 'usuario__email', 'legajo')
    ordering = ('sector', 'usuario__username',)

    def save_model(self, request, obj, form, change):
        """ Al guardar un empleado, actualizamos su estado de usuario asociado."""
        super().save_model(request, obj, form, change)

        user = obj.usuario
        user.is_staff = obj.activo
        user.is_superuser = False
        user.save()

        if obj.activo:
            # Asignar permisos según el sector del empleado.
            self._asignar_permisos(user, obj.sector)
        else:
            # Si el empleado no está activo, revocamos todos los permisos.
            user.user_permissions.clear()

    def _asignar_permisos(self, user, sector):
        """ Permisos específicos por sector. """
        from django.contrib.auth.models import Permission

        # Permisos comunes a todos los empleados.
        permisos_base = [
            'view_producto',
            'view_comentario',
            'delete_comentario',
            'view_supportticket',
            'change_supportticket',
        ]

        # Permisos adicionales por sector.
        permisos_sector = {
            'atencion al cliente': ['add_comentario', 'change_comentario'],
            'caja': ['add_comentario'],
            'reposicion': ['add_comentario'],
            'seguridad': ['view_empleado'],
            'limpieza': ['view_empleado'],
            'administracion': ['add_empleado', 'change_empleado', 'delete_empleado'],
        }
        # Combinamos permisos base con los específicos del sector.
        todos = permisos_base + permisos_sector.get(sector, [])
        
        # Asignamos los permisos al usuario.
        for codename in todos:
            try:
                perm = Permission.objects.get(codename=codename)
                user.user_permissions.add(perm)
            except Permission.DoesNotExit:
                pass  # Si el permiso no existe, lo ignoramos.