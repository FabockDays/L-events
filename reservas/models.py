from django.contrib.auth.models import User
from django.db import models



class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cantidad_invitados = models.IntegerField()
    fecha = models.DateField()
    hora_inicio = models.TimeField(default='00:00')
    hora_final = models.TimeField(default='00:00')
    TIPOS_DE_SALON = [
    ('con_catering', 'Con Catering'),
    ('solo_salon', 'Solo Salón'),
    ]
    
    tipo_salon = models.CharField(max_length=100, choices=TIPOS_DE_SALON)   

