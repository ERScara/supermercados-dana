from .models import Producto

def busqueda_global(request):
    query = request.GET.get('q', '').strip()
    resultados_busqueda = []

    if query:
        resultados_busqueda = Producto.objects.filter(
           nombre__icontains= query,
        )[:6]

    return {
        'resultados_busqueda': resultados_busqueda,
        'query_global': query,
    }