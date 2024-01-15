# Register your models here.
from django.contrib import admin
from .models import Reserva



class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cantidad_invitados', 'fecha', 'hora_inicio', 'hora_final', 'tipo_salon')

admin.site.register(Reserva, ReservaAdmin)

admin.site.site_header = "Panel de Administración"