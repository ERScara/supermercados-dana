from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.models import User, Permission
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import UpdateView
from .models import Cliente, SupportTicket, Comentario, VotoComentario, PreguntasFrecuentes
from empleados.models import Empleado
from .forms import PerfilForm, RegistroForm, ComentarioForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

def login_view(request):
    if request.user.is_authenticated:
        return redirect('productos:inicio')
    
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=usuario, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'productos:inicio')
                return redirect(next_url)
    return render(request, 'clientes/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('productos:inicio')

def registro(request):
    if request.user.is_authenticated:
        return redirect('productos:inicio')
    form = RegistroForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save()

            Cliente.objects.create(usuario=user)
            login(request, user)
            return redirect('productos:inicio')

    return render(request, 'clientes/registro.html', {'form': form })

def acerca_de(request):
    return render(request, 'acerca_de.html')

def reset_password(request):
    message = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email= request.POST.get('email', '').strip()

        try:
            user = User.objects.get(username=username, email=email)
            message = "Si los datos son correctos, recibirás un correo electrónico en breve."
        except User.DoesNotExist:
            message = "Si los datos son correctos, recibirás un correo electrónico en breve."
    
    return render(request, 'clientes/reset_password.html', {'message': message})

@login_required
def soporte(request):
    mensaje_enviado = False
    error_message = None
    reason = ''

    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        if not reason:
            error_message = 'Por favor, explica el motivo de tu solicitud'
        elif len(reason) > 3000:
            error_message = 'El mensaje no puede superar los 3000 caracteres (500 palabras aproxiamadamente).'
        else:
            SupportTicket.objects.create(
                username = request.user.username,
                email = request.user.email,
                reason = reason
            )
            # Nota práctica: en producción usaría send_mail() y se emplearía así
            """
            send_mail(
                subject=f'Solicitud de elimiación - {username}',
                message=f'Usuario: {username}\nEmail: {email}\n\nMotivo:\n{reason}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
            )
            """
            # como todavía estoy en modo desarrollo, esto no será empleado.

            mensaje_enviado = True

    return render(request, 'clientes/soporte.html', {
        'mensaje_enviado': mensaje_enviado,
        'error_mensaje': error_message,
        'reason': reason,
    })

class ComentarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'clientes/comentario_editar.html'
    success_url = reverse_lazy('clientes:inicio')

    def test_func(self):
        """ Solo el autor puede editar su comentario. """
        comentario = self.get_object()
        cliente = get_object_or_404(Cliente, usuario=self.request.user)
        return comentario.user == cliente and not comentario.is_deleted
    def handle_no_permission(self):
        return redirect('clientes:inicio')

@login_required
def hacerse_premium(request):
    if request.method == 'POST':
        cliente = Cliente.objects.get(usuario=request.user)
        if not cliente.es_cliente_premium:
            cliente.hacer_cliente_premium()

    return redirect('clientes:perfil')

@login_required
def perfil(request):
    cliente, _= Cliente.objects.get_or_create(usuario=request.user)
    cliente.refresh_from_db()

    if request.method == "POST":
        form = PerfilForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.email = form.cleaned_data.get('email', '')
            request.user.save()

            cliente.edad = form.cleaned_data.get('edad') or 0

            if 'avatar' in request.FILES:
                cliente.avatar = request.FILES['avatar']
            
            cliente.preferencias.set(form.cleaned_data.get('preferencias'))
            cliente.save()

            return redirect('clientes:perfil')
    else:
        form = PerfilForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'edad': cliente.edad,
            'preferencias': cliente.preferencias.all(),
        })
    
    historial = cliente.historial_compras.order_by('-cliente_id')[:5]

    context = {
        'form': form,
        'cliente': cliente,
        'historial': historial,
    }

    return render(request, 'clientes/perfil.html', context)

@login_required
def eliminar_avatar(request):
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, usuario=request.user)

        if cliente.avatar:
            import os
            if os.path.isfile(cliente.avatar.path):
                os.remove(cliente.avatar.path)
            cliente.avatar = None
            cliente.save()
    
    return redirect('clientes:perfil')
class PortalView(TemplateView):
    template_name= 'clientes/portal.html'

class FAQListView(ListView):
    model = PreguntasFrecuentes
    template_name = 'clientes/faq_list.html'
    context_object_name = 'preguntas'

class FAQDetailView(DetailView):
    model = PreguntasFrecuentes
    template_name = 'clientes/faq_detail.html'
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
    
    for comment in comentarios:
        voto = comment.votos.filter(cliente=cliente).first()
        comment.user_vote = voto.voto if voto else None
        
        comment.es_empleado = Empleado.objects.filter(
            usuario=comment.user.usuario,
            activo=True
        ).exists()
        
        for reply in comment.respuestas.all():
            voto_reply = reply.votos.filter(cliente=cliente).first()
            reply.user_vote = voto_reply.voto if voto_reply else None
            reply.es_empleado = Empleado.objects.filter (
                usuario=reply.user.usuario,
                activo=True
            ).exists()
    
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

    return render(request, 'clientes/portal.html', {
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
        return redirect('clientes:inicio')
    
    form = ComentarioForm(request.POST)
    if not form.is_valid():
        return redirect('clientes:inicio')  
    
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

    return redirect('clientes:inicio')
    
@login_required
def votar_comentario(request, comentario_id):
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
def reportar_comentario(request, comentario_id):
    """ Reportar un comentario. """
    if request.method != 'POST':
        return redirect('clientes:inicio')

    comentario = get_object_or_404(Comentario, pk=comentario_id)
    cliente = get_object_or_404(Cliente, usuario=request.user)

    if comentario.user and comentario.user.usuario and comentario.user.usuario.is_superuser:
        return redirect('clientes:inicio')
    
    if comentario.user != cliente:
        comentario.reportes.add(cliente)

    return redirect('clientes:inicio')
@login_required
def eliminar_comentario(request, comentario_id):
    """ Eliminar un comentario - solo el autor o el admin. """
    if request.method != 'POST':
        return redirect('clientes:inicio')

    comentario = get_object_or_404(Comentario, pk=comentario_id)
    cliente = get_object_or_404(Cliente, usuario=request.user)

    es_autor = comentario.user == cliente
    es_admin = request.user.is_superuser

    if es_autor or es_admin:
        comentario.is_deleted = True
        comentario.save()

    return redirect('clientes:inicio')