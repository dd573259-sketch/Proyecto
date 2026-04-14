from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

from app.models import (
    Usuario, Cliente, Producto, Plato,
    Venta, Factura, Pago, Pedido,
    Categoria, Mesa
)

# iniciamos cliente local
client = OpenAI(
    base_url="http://localhost:11434/",
    api_key="ollama"
)

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')

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

 #aca va contexto
            contexto = f"""
Eres el asistente virtual de La Taquería 

La Taquería es un sistema web desarrollado en Django para administrar un restaurante, se amable con los usuarios.

Módulos del sistema:
- Usuarios
- Clientes
- Productos
- Platos
- Categorías
- Mesas
- Pedidos
- Ventas
- Facturas
- Pagos

Datos actuales:
- Usuarios: {total_usuarios}
- Clientes: {total_clientes}
- Productos: {total_productos}
- Platos: {total_platos}
- Categorías: {total_categorias}
- Mesas: {total_mesas}
- Pedidos: {total_pedidos}
- Ventas: {total_ventas}
- Facturas: {total_facturas}
- Pagos: {total_pagos}

Instrucciones:
- Responde en español
- Sé amable y claro
- Máximo 2 renglones
- Si preguntan por el sistema, explica sus funciones
- Si no sabes algo, dilo honestamente
"""

            respuesta = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "kimi-k2.5:cloud",
                    "messages": [
                        {
                            "role": "system",
                            "content": contexto
                        },
                        {
                            "role": "user",
                            "content": message
                        }
                    ],
                    "stream": False
                }
            )

            resultado = respuesta.json()
            print("RESPUESTA:", resultado)

            texto = resultado.get("message", {}).get("content", "Sin respuesta")

            return JsonResponse({
                "response": texto
            })

        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({
                "error": str(e)
            }, status=500)

    return JsonResponse({
        "error": "Método no permitido"
    }, status=405)