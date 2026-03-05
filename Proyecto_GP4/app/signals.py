from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Plato, Producto, Menu
from .models import Pedido, Venta


@receiver(post_save, sender=Plato)
def crear_menu_plato(sender, instance, created, **kwargs):
    if created:
        Menu.objects.create(plato=instance)


@receiver(post_save, sender=Producto)
def crear_menu_producto(sender, instance, created, **kwargs):
    if created:
        Menu.objects.create(producto=instance)


# SIGNAL PARA CREAR VENTA CUANDO EL PEDIDO SE ENTREGA
@receiver(post_save, sender=Pedido)
def crear_venta_desde_pedido(sender, instance, created, **kwargs):

    if instance.estado == "Entregado":

        if not Venta.objects.filter(pedido=instance).exists():

            Venta.objects.create(
                usuario=instance.usuario,
                pedido=instance,
                total_venta=instance.total
            )