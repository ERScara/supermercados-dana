from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from .models import Empleado
from .forms import EmpleadoRegistroForm

def registro_empleado(request):
    """ Solo el superusuario puede crear empleados """
    if not request.user.is_superuser:
        return redirect('productos:inicio')
    
    form = EmpleadoRegistroForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data.get('username'),
                email = form.cleaned_data.get('email'),
                password = form.cleaned_data.get('password'),
                first_name = form.cleaned_data.get('first_name', ''),
                last_name = form.cleaned_data.get('last_name', ''),
            )
            user.is_staff = True
            user.is_superuser = False
            user.save()

            # Crear el empleado.
            empleado = Empleado.objects.create(
                usuario = user,
                legajo = form.cleaned_data.get('legajo'),
                sector = form.cleaned_data.get('sector'),
                activo = True
            )

            # Asignar permisos según sector.
            _asignar_permisos_empleado(user, empleado.sector)

            return redirect('empleados:lista_empleados')
    return render(request, 'empleados/registro_empleado.html', {
        'form': form
    })

def lista_empleados(request):
    """ Lista de empleados - solo para superusuario. """
    if not request.user.is_superuser:
        return redirect('productos:inicio')
    
    empleados = Empleado.objects.select_related('usuario').all()

    return render(request, 'empleados/lista_empleados.html', {
        'empleados': empleados
    })

def _asignar_permisos_empleado(user, sector):
    """ Función auxiliar para asignar permisos por sector. """
    permisos_base = [
        'view_producto',
        'view_comentario',
        'delete_comentario',
        'view_supportticket',
        'change_supportticket',
    ]

    permisos_sector = {
        'deposito': ['add_producto', 'change_producto', 'delete_producto'],
        'sistemas': ['add_producto', 'change_producto', 'delete_producto', 'add_categoria', 'change_categoria'],
        'atencion': ['view_cliente'],
        'caja': ['view_compra', 'view_carrito'],
    }
    
    todos = permisos_base + permisos_sector.get(sector, [])

    for codename in todos:
        try:
            ct = ContentType.objects.get_for_model(modelo)
            perm = Permission.objects.get(codename=codename)
            user.user_permissions.add(perm)
        except Permission.DoesNotExist:
            pass 