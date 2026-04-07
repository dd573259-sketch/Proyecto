# app/signals.py

from django.db.models.signals import post_save, post_delete

from django.dispatch import receiver
from .models import *


# ─────────────────────────────────────────────
#  SIGNALS EXISTENTES (Menu)
# ─────────────────────────────────────────────

@receiver(post_save, sender=Plato)
def crear_menu_plato(sender, instance, created, **kwargs):
    if created:
        Menu.objects.create(plato=instance)


@receiver(post_save, sender=Producto)
def crear_menu_producto(sender, instance, created, **kwargs):
    if created:
        Menu.objects.create(producto=instance)


# ─────────────────────────────────────────────
#  STOCK BAJO - PRODUCTO
# ─────────────────────────────────────────────

@receiver(post_save, sender=Producto)
def notificacion_stock_producto(sender, instance, **kwargs):
    if instance.stock <= 10:
        # Evita duplicados: solo crea si no hay una notificación activa (no leída)
        ya_existe = Notificacion.objects.filter(
            producto=instance,
            tipo_notificacion="Stock bajo",
            leido=False
        ).exists()

        if not ya_existe:
            if instance.stock == 0:
                mensaje = f"SIN STOCK: El producto '{instance.nombre}' está agotado."
            elif instance.stock < 5:
                mensaje = f"CRÍTICO: '{instance.nombre}' solo tiene {instance.stock} unidades."
            else:
                mensaje = f"Stock bajo: '{instance.nombre}' tiene {instance.stock} unidades."

            Notificacion.objects.create(
                producto=instance,
                tipo_notificacion="Stock bajo",
                mensaje=mensaje
            )
    else:
        # Si el stock se recuperó, elimina las notificaciones no leídas de ese producto
        Notificacion.objects.filter(
            producto=instance,
            tipo_notificacion="Stock bajo",
            leido=False
        ).delete()


# ─────────────────────────────────────────────
#  STOCK BAJO - INSUMO
# ─────────────────────────────────────────────

@receiver(post_save, sender=insumo)
def notificacion_stock_insumo(sender, instance, **kwargs):
    if instance.stock <= 10:
        ya_existe = Notificacion.objects.filter(
            insumo=instance,
            tipo_notificacion="Stock bajo",
            leido=False
        ).exists()

        if not ya_existe:
            if instance.stock == 0:
                mensaje = f"SIN STOCK: El insumo '{instance.nombre}' está re paila."
            elif instance.stock < 5:
                mensaje = f"CRÍTICO: '{instance.nombre}' solo tiene {instance.stock} unidades."
            else:
                mensaje = f"Stock bajo: '{instance.nombre}' tiene {instance.stock} unidades."

            Notificacion.objects.create(
                insumo=instance,
                tipo_notificacion="Stock bajo",
                mensaje=mensaje
            )
    else:
        # Si el stock se recuperó, limpia notificaciones no leídas de ese insumo
        Notificacion.objects.filter(
            insumo=instance,
            tipo_notificacion="Stock bajo",
            leido=False
        ).delete()


# ─────────────────────────────────────────────
#  USUARIOS - Crear / Editar / Eliminar
# ─────────────────────────────────────────────

@receiver(post_save, sender=Usuario)
def notificacion_usuario_guardado(sender, instance, created, **kwargs):
    if created:
        Notificacion.objects.create(
            usuario=instance,
            tipo_notificacion="Usuario creado",
            mensaje=f"Nuevo usuario registrado: '{instance.nombre} {instance.apellido}' con rol '{instance.rol}'."
        )
    else:
        Notificacion.objects.create(
            usuario=instance,
            tipo_notificacion="Usuario editado",
            mensaje=f"El usuario '{instance.nombre} {instance.apellido}' fue modificado."
        )


@receiver(post_delete, sender=Usuario)
def notificacion_usuario_eliminado(sender, instance, **kwargs):
    # Al eliminar el usuario, el FK se pone en NULL gracias a on_delete=CASCADE no aplica aquí,
    # pero creamos la notificación ANTES de que el objeto desaparezca — post_delete lo permite
    Notificacion.objects.create(
        usuario=None,  # ya no existe, evitamos FK roto
        tipo_notificacion="Usuario eliminado",
        mensaje=f"El usuario '{instance.nombre} {instance.apellido}' (rol: {instance.rol}) fue eliminado del sistema."
    )