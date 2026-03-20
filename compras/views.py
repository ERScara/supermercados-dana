from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Compra, ItemCompra
from .forms import CheckoutForm
from carrito.models import Carrito
from clientes.models import Cliente

@login_required(login_url='clientes:login')
def checkout(request):
    cliente = get_object_or_404(Cliente, usuario=request.user)
    carrito = get_object_or_404(Carrito, cliente=cliente)

    if not carrito.items.exists():
        return redirect('carrito:ver')
    
    form = CheckoutForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            numero = form.cleaned_data['numero_tarjeta'].replace(' ', '')
            ultimos_4 = numero[-4:]

            compra = Compra.objects.create(
                cliente = cliente,
                total = carrito.total(),
                estado='aprobada',
                ultimos_4_digitos = ultimos_4
            )

            for item in carrito.items.all():
                ItemCompra.objects.create(
                    compra = compra,
                    producto= item.producto,
                    cantidad=item.cantidad,
                    precio_unitario=item.precio_unitario,
                    precio_original=item.producto.precio
                )
                item.producto.stock -= item.cantidad
                item.producto.save()

            carrito.vaciar()

            return redirect('compras:confirmar', compra_id=compra.id)

    return render(request, 'compras/checkout.html', {
        'form': form,
        'carrito': carrito,
        'items': carrito.items.select_related('producto').all()
    })

@login_required(login_url='clientes:login')
def confirmar(request, compra_id):
    cliente = get_object_or_404(Cliente, usuario=request.user)
    compra = get_object_or_404(Compra, id=compra_id, cliente=cliente)

    items = compra.items.select_related('producto').all()
    for item in items:
        _ = item.ahorro

    return render(request, 'compras/confirmar.html', {
        'compra': compra,
        'items': compra.items.select_related('producto').all(),
    })