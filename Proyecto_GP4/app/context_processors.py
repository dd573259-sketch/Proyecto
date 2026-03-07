from .models import Notificacion


def notificaciones_admin(request):
    if request.user.is_authenticated:

        notificaciones = Notificacion.objects.filter(
            leido=False
        )

        return {
            'contador_notificaciones': notificaciones.count()
        }
    return {'contador_notificaciones': 0}