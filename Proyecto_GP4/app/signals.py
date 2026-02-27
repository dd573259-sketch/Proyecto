from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Plato, Producto, Menu


@receiver(post_save, sender=Plato)
def crear_menu_plato(sender, instance, created, **kwargs):
    if created:
        Menu.objects.create(plato=instance)


@receiver(post_save, sender=Producto)
def crear_menu_producto(sender, instance, created, **kwargs):
    if created:
        Menu.objects.create(producto=instance)
