# app/context_processors.py

from .models import Notificacion

def notificaciones_admin(request):
    # Cuenta TODAS las notificaciones no leídas (no filtra por usuario)
    # porque las de stock y sistema no tienen usuario asignado
    contador = Notificacion.objects.filter(leido=False).count()
    
    return {
        'contador_notificaciones': contador
    }
