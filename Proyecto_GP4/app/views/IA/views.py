import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ollama import chat

from app.models import (
    Usuario, Cliente, Producto, Plato,
    Venta, Factura, Pago, Pedido,
    Categoria, Mesa
)

@csrf_exempt
def chat_view(request):
    print(request.method)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()

            # ==========================
            # DETECTAR MODO SECRETO
            # ==========================
            modo_contexto = message.startswith("12345")
            mensaje_limpio = message.replace("12345", "").strip().lower()

            # ==========================
            # DATOS REALES DEL SISTEMA
            # ==========================
            total_usuarios = Usuario.objects.count()
            total_clientes = Cliente.objects.count()
            total_productos = Producto.objects.count()
            total_platos = Plato.objects.count()
            total_ventas = Venta.objects.count()
            total_facturas = Factura.objects.count()
            total_pagos = Pago.objects.count()
            total_pedidos = Pedido.objects.count()
            total_categorias = Categoria.objects.count()
            total_mesas = Mesa.objects.count()

            # ==========================
            # SALUDOS
            # ==========================
            if mensaje_limpio in ["hola", "buenas", "hello", "hi"]:
                return JsonResponse({"response": "Hola, ¿en qué puedo ayudarte?"})

            # ==========================
            # INTENCIONES (DÓNDE HACER ALGO)
            # ==========================
            if any(p in mensaje_limpio for p in ["donde", "dónde"]):

                if any(w in mensaje_limpio for w in ["pedido", "pedidos"]):
                    return JsonResponse({"response": "Puedes crear un pedido en el módulo de Pedidos."})

            elif any(w in mensaje_limpio for w in ["venta", "ventas"]):
                return JsonResponse({"response": "Puedes registrar una venta en el módulo de Ventas."})

            elif any(w in mensaje_limpio for w in ["cliente", "clientes"]):
                return JsonResponse({"response": "Puedes gestionar clientes en el módulo de Clientes."})

            elif any(w in mensaje_limpio for w in ["producto", "productos"]):
                return JsonResponse({"response": "Puedes gestionar productos en el módulo de Productos."})

            elif any(w in mensaje_limpio for w in ["factura", "facturas"]):
                return JsonResponse({"response": "Puedes generar facturas en el módulo de Facturas."})

            elif any(w in mensaje_limpio for w in ["pago", "pagos"]):
                return JsonResponse({"response": "Puedes registrar pagos en el módulo de Pagos."})

            elif any(w in mensaje_limpio for w in ["mesa", "mesas"]):
                return JsonResponse({"response": "Puedes gestionar mesas en el módulo de Mesas."})

            # ==========================
            # RESPUESTAS DIRECTAS (CONTEO)
            # ==========================
            if "venta" in mensaje_limpio:
                return JsonResponse({"response": f"Hay {total_ventas} ventas."})

            elif "cliente" in mensaje_limpio:
                return JsonResponse({"response": f"Hay {total_clientes} clientes."})

            elif "pedido" in mensaje_limpio:
                return JsonResponse({"response": f"Hay {total_pedidos} pedidos."})

            elif "producto" in mensaje_limpio:
                return JsonResponse({"response": f"Hay {total_productos} productos."})

            elif "usuario" in mensaje_limpio:
                return JsonResponse({"response": f"Hay {total_usuarios} usuarios."})

            elif "mesa" in mensaje_limpio:
                return JsonResponse({"response": f"Hay {total_mesas} mesas."})

            elif "factura" in mensaje_limpio:
                return JsonResponse({"response": f"Hay {total_facturas} facturas."})

            elif "pago" in mensaje_limpio:
                return JsonResponse({"response": f"Hay {total_pagos} pagos."})

            # ==========================
            # CONTEXTO BASE
            # ==========================
            contexto = f"""
Eres el asistente virtual de La Taquería.

Sistema web en Django para administrar un restaurante.

Datos actuales:
Usuarios: {total_usuarios}
Clientes: {total_clientes}
Productos: {total_productos}
Platos: {total_platos}
Categorías: {total_categorias}
Mesas: {total_mesas}
Pedidos: {total_pedidos}
Ventas: {total_ventas}
Facturas: {total_facturas}
Pagos: {total_pagos}
"""

            # ==========================
            # INSTRUCCIONES
            # ==========================
            instrucciones = f"""
MODO CONTEXTO: {"ACTIVO" if modo_contexto else "INACTIVO"}

REGLAS:
- RESPONDE ÚNICAMENTE EN ESPAÑOL.
- MÁXIMO 2 LÍNEAS.
- NO INVENTES INFORMACIÓN.
- RESPONDE CLARO Y DIRECTO.
"""

            # ==========================
            # LLAMADA A OLLAMA (LOCAL)
            # ==========================
            response = chat(
                model='deepseek-coder:latest',
                messages=[
                    {"role": "system", "content": contexto + instrucciones},
                    {"role": "user", "content": mensaje_limpio}
                ],
                options={
                    "num_predict": 50,
                    "temperature": 0.2,
                    "top_k": 20
                }
            )

            texto = response['message']['content']

            return JsonResponse({
                "response": texto
            })

        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=500)

    return JsonResponse({
        "error": "Método no permitido"
    }, status=405)