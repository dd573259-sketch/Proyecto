# app/utils_email.py
import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

def enviar_alerta_vencimiento(producto, dias_restantes):
    """
    Envia un correo de alerta por vencimiento de producto.
    Retorna True si se envio correctamente, False en caso de error.
    """
    if dias_restantes < 0:
        asunto = f"ALERTA: Producto VENCIDO - {producto.nombre}"
        cuerpo = (
            f"El producto '{producto.nombre}' (ID: {producto.id_producto}) vencio el {producto.fecha_vencimiento}.\n"
            f"Por favor retiralo del inventario y actualiza el stock."
        )
    elif dias_restantes == 0:
        asunto = f"ALERTA: Producto vence HOY - {producto.nombre}"
        cuerpo = (
            f"El producto '{producto.nombre}' vence hoy {producto.fecha_vencimiento}.\n"
            f"Toma accion inmediata."
        )
    else:
        asunto = f"ALERTA: Producto proximo a vencer - {producto.nombre}"
        cuerpo = (
            f"El producto '{producto.nombre}' vence en {dias_restantes} dias ({producto.fecha_vencimiento}).\n"
            f"Revisa el inventario y considera su uso o reubicacion."
        )

    # Lista de destinatarios
    destinatarios = [settings.EMAIL_HOST_USER]

    try:
        send_mail(
            asunto,
            cuerpo,
            settings.EMAIL_HOST_USER,
            destinatarios,
            fail_silently=False,
        )
        logger.info(f"Correo enviado para {producto.nombre} - {asunto}")
        return True
    except Exception as e:
        logger.error(f"Error al enviar correo para {producto.nombre}: {str(e)}")
        return False