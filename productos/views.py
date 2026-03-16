from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria

def inicio(request):
    categorias = Categoria.objects.all()
    productos_destacados = Producto.objects.filter(stock__gt=0)[:6]
    context = {
        'categorias': categorias,
        'prodcutos_destacados': productos_destacados,
    }
    return render(request, 'inicio.html', context)

def lista_productos(request):
    categoria_id = request.GET.get('categoria')
    productos = Producto.objects.filter(stock__gt=0)
    categorias = Categoria.objects.all()
    categoria_activa = None
    if categoria_id:
        categoria_activa = Categoria.objects.filter(id=categoria_id).first()
        if categoria_activa:           
            productos = productos.filter(categoria__id=categoria_id)
    cliente = None
    if request.user.is_authenticated:
        from clientes.models import Cliente
        cliente = Cliente.objects.filter(usuario=request.user).first()
    context = {
        'productos': productos,
        'categorias': categorias,
        'categoria_activa': categoria_activa,
        'cliente': cliente,
    }
    return render(request, 'productos/lista.html', context)

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    cliente = None
    if request.user.is_authenticated:
        from clientes.models import Cliente
        cliente = Cliente.objects.filter(usuario=request.user).first()
    return render(request, 'productos/detalle.html', {
        'producto': producto,
        'cliente': cliente,
        })

def buscar(request):
    query = request.GET.get('q', '').strip()
    resultados = []
    
    if query:
        resultados = Producto.objects.filter(
            nombre__icontains=query,
            stock__gt=0
        ) | Producto.objects.filter(
            descripcion__icontains=query,
            stock__gt=0
        ) 
        resultados = resultados.distinct()

    cliente = None;
    if request.user.is_authenticated:
        from clientes.models import Cliente
        cliente = Cliente.objects.filter(usuario=request.user).first()

    context = {
        'resultados': resultados,
        'query': query,
        'cliente': cliente,
    }
    return render(request, 'productos/buscar.html', context)
    
