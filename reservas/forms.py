from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reserva
from django.utils import timezone



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Eliminar mensajes de validación específicos para los campos 
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None

        # personalizar los labels 
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['first_name'].label = 'Nombre'
        self.fields['last_name'].label = 'Apellido'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirmar Password'

        # Hacer los campos de nombre y apellido obligatorios
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

         # Agregar placeholders
        self.fields['username'].widget.attrs['placeholder'] = 'Sólo letras, dígitos y @/./+/-/_.'
        self.fields['password1'].widget.attrs['placeholder'] = 'Al menos 8 caracteres / No puede ser totalmente numérica.'
        

 


class ReservaForm(forms.ModelForm):

    hora_inicio = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'hora-input'}))
    hora_final = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'hora-input'}))
    cantidad_invitados = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': '1', 'max': '2500', 'class': 'invitados-input', 'placeholder': 'Cantidad de personas'}))
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'fecha-input'}))
    

    class Meta:
        model = Reserva
        fields = ['cantidad_invitados', 'tipo_salon',
                  'fecha', 'hora_inicio', 'hora_final']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),  
            'cantidad_invitados': forms.NumberInput(attrs={'min': '1', 'max' : '2500'})
        }

    def clean_cantidad_invitados(self):
        cantidad_invitados = self.cleaned_data['cantidad_invitados']
        if cantidad_invitados < 1 or cantidad_invitados > 2500:
            raise forms.ValidationError(
                "La cantidad de invitados debe estar entre 1 y 2500.")
        return cantidad_invitados

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < timezone.now().date():
            raise forms.ValidationError(
                "No puedes elegir una fecha anterior al día actual.")

        reservas_en_fecha = Reserva.objects.filter(fecha=fecha)
        if reservas_en_fecha.exists():
            raise forms.ValidationError("Esta fecha ya está reservada.")

        return fecha

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_final = cleaned_data.get('hora_final')

        # Verificar si se han proporcionado ambas horas
        if hora_inicio and hora_final:
            # Comprobar si la hora de inicio y la hora final coinciden
            if hora_inicio == hora_final:
                raise forms.ValidationError(
                    "La hora de inicio y la hora final no pueden ser iguales."
                )

            # Verificar si la hora de inicio es posterior a la hora final
            if hora_inicio > hora_final:
                raise forms.ValidationError(
                    "La hora de inicio no puede ser posterior a la hora final."
                )

        return cleaned_data

    
    