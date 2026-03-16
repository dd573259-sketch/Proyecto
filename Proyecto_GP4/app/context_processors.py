# app/context_processors.py

from .models import Notificacion

def notificaciones_admin(request):
    contador = Notificacion.objects.filter(leido=False).count()
    notificaciones_recientes = Notificacion.objects.filter(
        leido=False
    ).order_by('-fecha')[:5]  # últimas 5 no leídas

    return {
        'contador_notificaciones': contador,
        'notificaciones_recientes': notificaciones_recientes,
    }