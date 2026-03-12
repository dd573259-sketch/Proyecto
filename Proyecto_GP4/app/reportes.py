from django.shortcuts import render
from django.views import View as DjangoView
from app.models import Pedido
from app.utils import exportar_pdf, exportar_excel
from datetime import datetime
from django.utils import timezone


# ====== EXPORTAR PEDIDOS A PDF ======

class ExportarpedidoPDF(DjangoView):

    def get(self, request):

        pedidos = Pedido.objects.all()

        columnas = ['ID', 'MESA', 'PLATOS', 'PRODUCTOS', 'USUARIO', 'FECHA', 'ESTADO', 'TOTAL']

        datos = []

        for pedido in pedidos:

            platos = ", ".join([
                detalle.plato.nombre for detalle in pedido.detalle_platos.all()
            ])

            productos = ", ".join([
                detalle.producto.nombre for detalle in pedido.detalle_productos.all()
            ])

            datos.append(
                (
                    pedido.id_pedido,
                    pedido.mesa.numero_mesa,
                    platos,
                    productos,
                    pedido.usuario,
                    pedido.fecha_hora,
                    pedido.estado,
                    pedido.total
                )
            )

        nombre_archivo = f'Reporte_Pedidos_{datetime.now().strftime("%d_%m_%Y")}'

        return exportar_pdf(
            titulo='REPORTE DE PEDIDOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )


# ====== EXPORTAR PEDIDOS A EXCEL ======

class ReportePedidosExcel(DjangoView):

    def get(self, request):

        pedidos = Pedido.objects.all()

        columnas = ['ID', 'MESA', 'PLATOS', 'PRODUCTOS', 'USUARIO', 'FECHA', 'ESTADO', 'TOTAL']

        datos = []

        for pedido in pedidos:

            platos = ", ".join([
                detalle.plato.nombre for detalle in pedido.detalle_platos.all()
            ])

            productos = ", ".join([
                detalle.producto.nombre for detalle in pedido.detalle_productos.all()
            ])

            datos.append(
                (
                    pedido.id_pedido,
                    pedido.mesa.numero_mesa,
                    platos,
                    productos,
                    str(pedido.usuario),
                    timezone.localtime(pedido.fecha_hora).strftime("%d/%m/%Y %H:%M"),
                    pedido.estado,
                    pedido.total
                )
            )

        nombre_archivo = f'Reporte_Pedidos_{datetime.now().strftime("%d_%m_%Y")}'

        return exportar_excel(
            titulo='REPORTE DE PEDIDOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )