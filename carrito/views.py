from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Carrito, ItemCarrito
from productos.models import Producto
from clientes.models import Cliente 

@login_required(login_url='clientes:login')
def ver_carrito(request):
    cliente = get_object_or_404(Cliente, usuario=request.user)
    carrito, _= Carrito.objects.get_or_create(cliente=cliente)

    return render(request, 'carrito/carrito.html', {
        'carrito': carrito,
        'items': carrito.items.select_related('producto').all()
    })

@login_required(login_url='clientes:login')
def agregar(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, pk=producto_id)
        cliente = get_object_or_404(Cliente, usuario=request.user)
        carrito, _ = Carrito.objects.get_or_create(cliente=cliente)
        
        if cliente.es_cliente_premium:
            precio = producto.precio_con_descuento
        else:
            precio = producto.precio
        
        item, creado = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={'precio_unitario': precio, 'cantidad': 1}
        )

        if not creado:
            if item.cantidad < producto.stock:
                item.cantidad += 1
                item.save()

    return redirect('carrito:ver')

@login_required(login_url='clientes:login')
def eliminar(request, producto_id):
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, usuario=request.user)
        carrito = get_object_or_404(Carrito, cliente= cliente)
        item = get_object_or_404(
           ItemCarrito,
           carrito=carrito,
           producto__id = producto_id
        )
        item.delete()

    return redirect('carrito:ver')

@login_required(login_url='clientes:login')
def actualizar_cantidad(request, producto_id):
    """ Aumenta o disminuye la cantidad de un item. """
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, usuario=request.user)
        carrito = get_object_or_404(Carrito, cliente=cliente)
        item = get_object_or_404(
            ItemCarrito,
            carrito=carrito,
            producto__id=producto_id
        )
        accion = request.POST.get('accion')

        if accion == 'sumar' and item.cantidad < item.producto.stock:
            item.cantidad += 1
            item.save()
        elif accion == 'restar':
            if item.cantidad > 1:
                item.cantidad -= 1
                item.save()
            else: 
                item.delete()
    
    return redirect('carrito:ver')