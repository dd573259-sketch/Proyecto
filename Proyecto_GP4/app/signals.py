from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Plato, Producto, Menu
from .models import Producto, Notificacion, Usuario


@receiver(post_save, sender=Plato)
def crear_menu_plato(sender, instance, created, **kwargs):
    if created:
        Menu.objects.create(plato=instance)


@receiver(post_save, sender=Producto)
def crear_menu_producto(sender, instance, created, **kwargs):
    if created:
        Menu.objects.create(producto=instance)

@receiver(post_save, sender=Producto)
def notificacion_stock_bajo(sender, instance, **kwargs):

    if instance.stock <= 10:

        admins = Usuario.objects.filter(rol="Administrador")

        for admin in admins:

            Notificacion.objects.create(
                usuario=admin,
                producto=instance,
                tipo_notificacion="Stock Bajo",
                mensaje=f"El producto {instance.nombre} tiene solo {instance.stock} unidades"
            )
