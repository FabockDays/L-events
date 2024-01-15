from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import Reserva
from .forms import ReservaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.contrib.auth import logout as django_logout


def home(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Autenticar al usuario después del registro

            return redirect('formulario_invitados')
    else:
        form = UserRegistrationForm()
        messages.error(
                request, 'Error en el formulario. Por favor, verifique los datos.')
    return render(request, 'home.html', {'form': form})


@login_required
def formulario_invitados(request):
    reserva_exitosa = False
    fecha_reservada = False
    fechas_reservadas = []

    user = request.user

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            nueva_reserva = form.save(commit=False)
            fecha_reservada = Reserva.objects.filter(
                fecha=nueva_reserva.fecha).exists()
            if not fecha_reservada:
                nueva_reserva.usuario = user
                nueva_reserva.save()
                reserva_exitosa = True
                # Limpiar el formulario después de una reserva exitosa
                form = ReservaForm()
            else:
                messages.error(
                    request, 'Lo siento, esta fecha ya ha sido reservada.')
        else:
            messages.error(
                request, 'Error en el formulario. Por favor, verifique los datos.')
    else:
        # Si no es una solicitud POST, crear un formulario nuevo
        form = ReservaForm()

    fechas_reservadas = Reserva.objects.values_list('fecha', flat=True)

    form.fields['fecha'].widget.attrs.update({
        'min': timezone.now().date(),
        'data-reserved-dates': ','.join(map(str, fechas_reservadas)),
    })

    if request.method == 'GET' and 'logout' in request.GET:
        django_logout(request)
        return redirect('home')

    return render(request, 'formulario_invitados.html', {
        'form': form,
        'reserva_exitosa': reserva_exitosa,
        'fechas_reservadas': fechas_reservadas,
        'user_registered': user,
    })


def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        remember_me = request.POST.get('remember')   # Valor del checkbox

        # Autenticar al usuario con las credenciales proporcionadas
        user = authenticate(request, username=email, password=password)

        if user:
            # Si el usuario se autentica correctamente, iniciar sesión
            login(request, user)

            return redirect('formulario_invitados')
        else:
            error_message = "Usuario o contraseña incorrectos. Por favor, intenta de nuevo."
            return render(request, 'registration/login.html', {'error_message': error_message})

    return render(request, 'registration/login.html')
