from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch
from django.http import JsonResponse
from .models import Comentario, VotoComentario, PreguntasFrecuentes
from .forms import ComentarioForm
from clientes.models import Cliente

class PortalView(TemplateView):
    template_name= 'atencion_cliente/portal.html'

class FAQListView(ListView):
    model = PreguntasFrecuentes
    template_name = 'atencion_cliente/faq_list.html'
    context_object_name = 'preguntas'

class FAQDetailView(DetailView):
    model = PreguntasFrecuentes
    template_name = 'atencion_cliente/faq_detail.html'
    context_object_name = 'pregunta'

def inicio(request):
    orden = request.GET.get('orden', 'newest')
    comentarios = Comentario.objects.filter(
        is_deleted=False,
        parent__isnull=True
    ).select_related('user', 'parent').prefetch_related('votos', 'reportes', 'respuestas__votos', 'respuestas__reportes')

    if orden == 'oldest':
        comentarios = comentarios.order_by('fecha')
    elif orden == 'best':
        comentarios = comentarios.order_by('-puntuacion', 'fecha')
    elif orden == 'worst':
        comentarios = comentarios.order_by('puntuacion', 'fecha')
    else:
        comentarios = comentarios.order_by('-fecha')
        orden = 'newest'

    cliente = Cliente.objects.filter(usuario=request.user).first() if request.user.is_authenticated else None

    if cliente:
        for comment in comentarios:
            voto = comment.votos.filter(cliente=cliente).first()
            comment.user_vote = voto.voto if voto else None

            for reply in comment.respuestas.all():
                voto_reply = reply.votos.filter(cliente=cliente).first()
                reply.user_vote = voto_reply.voto if voto_reply else None
    
    total = comentarios.count()
    promedio = round(sum(c.puntuacion for c in comentarios) / total, 1) if total > 0 else 0
    form = ComentarioForm() if request.user.is_authenticated else None

    return render(request, 'atencion_cliente/portal.html', {
        'comentarios': comentarios,
        'total': total,
        'promedio': promedio,
        'form': form,
        'orden': orden,
        'cliente': cliente,
    })

def crear_comentario(request):
    """ Comentario que los clientes hacen en el área de atención al cliente. """

    if request.method != 'POST':
        return redirect('atencion_cliente:inicio')
    
    form = ComentarioForm(request.POST)
    if not form.is_valid():
        return redirect('atencion_cliente:inicio')  
    
    cliente = get_object_or_404(Cliente, usuario=request.user)

    comentario = form.save(commit=False)
    comentario.user = cliente

    parent_id = request.POST.get('parent_id')
    
    if parent_id:
        try:
            parent = Comentario.objects.get(id=parent_id)
            comentario.parent = parent
        except Comentario.DoesNotExist:
            pass
    
    comentario.save()

    return redirect('atencion_cliente:inicio')
    
@login_required
def votar(request, comentario_id):
    """ Me gusta / No me gusta en un comentario. Vía AJAX. """

    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    cliente = get_object_or_404(Cliente, usuario=request.user)
    voto= request.POST.get('voto')

    if voto not in ['like', 'dislike']:
        return JsonResponse({'error': 'Voto inválido'}, status=400)
    
    voto_obj, creado = VotoComentario.objects.get_or_create(
        comentario=comentario,
        cliente=cliente,
        defaults={'voto':voto}
    )

    if not creado:
        if voto_obj.voto == voto:
            voto_obj.delete()
        else:
            voto_obj.voto = voto
            voto_obj.save()

    voto_actual = VotoComentario.objects.filter(
        comentario = comentario,
        cliente = cliente
    ).first()

    user_vote = voto_actual.voto if voto_actual else None

    return JsonResponse({
        'likes': comentario.votos.filter(voto='like').count(),
        'dislikes': comentario.votos.filter(voto='dislike').count(),
        'user_vote': user_vote,
    })

@login_required
def reportar(request, comentario_id):
    """ Reportar un comentario. """
    if request.method != 'POST':
        return redirect('atencion_cliente:inicio')

    comentario = get_object_or_404(Comentario, pk=comentario_id)
    cliente = get_object_or_404(Cliente, usuario=request.user)

    if comentario.user and comentario.user.usuario and comentario.user.usuario.is_superuser:
        return redirect('atencion_cliente:inicio')
    
    if comentario.user != cliente:
        comentario.reportes.add(cliente)

    return redirect('atencion_cliente:inicio')


@login_required
def eliminar(request, comentario_id):
    """ Eliminar un comentario - solo el autor o el admin. """
    if request.method != 'POST':
        return redirect('atencion_cliente:inicio')

    comentario = get_object_or_404(Comentario, pk=comentario_id)
    cliente = get_object_or_404(Cliente, usuario=request.user)

    es_autor = comentario.user == cliente
    es_admin = request.user.is_superuser

    if es_autor or es_admin:
        comentario.is_deleted = True
        comentario.save()

    return redirect('atencion_cliente:inicio')