from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Cliente, SupportTicket
from .forms import PerfilForm, RegistroForm

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
    
    return render(request, 'clientes/login.html', { 'form': form })

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