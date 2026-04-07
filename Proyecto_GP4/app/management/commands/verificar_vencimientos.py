# app/management/commands/verificar_vencimientos.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from app.models import Producto, Notificacion


class Command(BaseCommand):
    help = 'Verifica productos próximos a vencer'

    def handle(self, *args, **kwargs):
        hoy = timezone.now().date()

        for producto in Producto.objects.all():
            if not producto.fecha_vencimiento:
                continue

            dias_restantes = (producto.fecha_vencimiento - hoy).days

            # ── Ya venció ──
            if dias_restantes < 0:
                ya_existe = Notificacion.objects.filter(
                    producto=producto,
                    tipo_notificacion="Producto vencido",
                    leido=False
                ).exists()
                if not ya_existe:
                    Notificacion.objects.create(
                        producto=producto,
                        tipo_notificacion="Producto vencido",
                        mensaje=f"⛔ VENCIDO: '{producto.nombre}' venció el {producto.fecha_vencimiento}."
                    )
                    self._enviar_correo(producto, dias_restantes)

            # ── Vence hoy ──
            elif dias_restantes == 0:
                ya_existe = Notificacion.objects.filter(
                    producto=producto,
                    tipo_notificacion="Vence hoy",
                    leido=False
                ).exists()
                if not ya_existe:
                    Notificacion.objects.create(
                        producto=producto,
                        tipo_notificacion="Vence hoy",
                        mensaje=f"🚨 '{producto.nombre}' vence HOY {producto.fecha_vencimiento}."
                    )
                    self._enviar_correo(producto, dias_restantes)

            # ── Próximo a vencer (8 días antes) ──
            elif dias_restantes <= 8:
                ya_existe = Notificacion.objects.filter(
                    producto=producto,
                    tipo_notificacion="Próximo a vencer",
                    leido=False
                ).exists()
                if not ya_existe:
                    Notificacion.objects.create(
                        producto=producto,
                        tipo_notificacion="Próximo a vencer",
                        mensaje=f"⚠️ '{producto.nombre}' vence en {dias_restantes} días ({producto.fecha_vencimiento})."
                    )
                    self._enviar_correo(producto, dias_restantes)

        self.stdout.write(self.style.SUCCESS('✅ Verificación completada'))

    def _enviar_correo(self, producto, dias_restantes):
        if dias_restantes < 0:
            asunto = f"⛔ Producto VENCIDO: {producto.nombre}"
            cuerpo = f"El producto '{producto.nombre}' venció el {producto.fecha_vencimiento}. Por favor retíralo del inventario."
        elif dias_restantes == 0:
            asunto = f"🚨 Producto vence HOY: {producto.nombre}"
            cuerpo = f"El producto '{producto.nombre}' vence hoy {producto.fecha_vencimiento}."
        else:
            asunto = f"⚠️ Producto próximo a vencer: {producto.nombre}"
            cuerpo = f"El producto '{producto.nombre}' vence en {dias_restantes} días ({producto.fecha_vencimiento})."

        try:
            send_mail(
                asunto,
                cuerpo,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error enviando correo: {e}'))