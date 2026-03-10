from django.shortcuts import render
from django.views.generic import View
from django.views import View as DjangoView
from django.http import HttpResponse
from app.models import *
from app.utils import exportar_pdf, exportar_excel
from datetime import datetime



# ====== VISTAS PARA EXPORTAR REPORTES ======

class ExportarventasPDF(DjangoView):
    """
    VISTA PARA EXPORTAR VENTAS A PDF
    Obtiene todas las ventas y las exporta en formato PDF
    """
    
    def get(self, request):
        # Obtener todas las ventas
        ventas = Venta.objects.all()
        
        # Definir las columnas que se muestran en el reporte
        columnas = ['ID', 'Usuario', 'Pedido', 'Total', 'Fecha']
        
        # Preparar los datos en formato de tuplas
        datos = [
            (venta.id_venta, venta.usuario, venta.pedido, venta.total, venta.fecha_venta)
            for venta in ventas
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Ventas_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a PDF
        return exportar_pdf(
            titulo='REPORTE DE VENTAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
    


class ExportarventasExcel(DjangoView):
    """
    VISTA PARA EXPORTAR VENTAS A EXCEL
    Obtiene todas las ventas y las exporta en formato Excel
    """
    
    def get(self, request):
        # Obtener todas las ventas
        ventas = Venta.objects.all()
        
        # Definir las columnas que se mostraran en el reporte
        columnas = ['ID', 'Usuario', 'Pedido', 'Total', 'Fecha']
        
        # Preparar los datos en  tuplas
        datos = [
            (venta.id_venta, str(venta.usuario), str(venta.pedido), venta.total, venta.fecha_venta.replace(tzinfo=None))
            for venta in ventas
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Ventas_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE VENTAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
    


#-------------------------------------------------------------------------------
#=======ESTAS SON LAS VISTAS O CLASES PARA CREAR EL REPORTE DE PAGOS============
#-------------------------------------------------------------------------------

class ExportarpagosPDF(DjangoView):
    """
    VISTA PARA EXPORTAR PAGOS A PDF
    Obtiene todos los pagos y los exporta en formato PDF
    """
    
    def get(self, request):
        # Obtener todos los pagos
        pagos = Pago.objects.all()
        
        # Definir las columnas que se muestran en el reporte
        columnas = ['ID', 'Venta', 'Factura', 'Total venta ', 'Monto pagado ', 'Fecha', 'Metodo de pago']
        
        # Preparar los datos en formato de tuplas
        datos = [
            (pago.id_pago, pago.venta, pago.factura, pago.venta.total, pago.monto, pago.fecha, pago.metodo_pago)
            for pago in pagos
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Pagos_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a PDF
        return exportar_pdf(
            titulo='REPORTE DE PAGOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
#======================================================================================



class ExportarpagosExcel(DjangoView):
    """
    VISTA PARA EXPORTAR PAGOS A EXCEL
    Obtiene todos los pagos y los exporta en formato Excel
    """
    
    def get(self, request):
        # Obtener todos los pagos
        pagos = Pago.objects.all()
        
        # Definir las columnas que se muestran en el reporte
        columnas = ['ID', 'Venta', 'Factura', 'Total venta ', 'Monto pagado ', 'Fecha', 'Metodo de pago']
        
        # Preparar los datos en formato de tuplas
        datos = [
            (pago.id_pago, pago.venta, pago.factura, pago.venta.total, pago.monto, pago.fecha, pago.metodo_pago)
            for pago in pagos
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Pagos_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE PAGOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
        
#======================================================================================



#=======ESTAS SON LAS VISTAS O CLASES PARA CREAR EL REPORTE DE FACTURAS============

class ExportarfacturasPDF(DjangoView):
    """
    VISTA PARA EXPORTAR FACTURAS A PDF
    Obtiene todas las facturas y las exporta en formato PDF
    """
    
    def get(self, request):
        # Obtener todas las facturas
        facturas = Factura.objects.all()
        
        # Definir las columnas que se muestran en el reporte
        columnas = ['ID', 'Venta', 'Total', 'Método de pago', 'Fecha']
        
        # Preparar los datos en formato de tuplas
        datos = [
            (factura.id, factura.venta, factura.valor_total, factura.metodo_pago, factura.fecha_hora)
            for factura in facturas
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Facturas_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a PDF
        return exportar_pdf(
            titulo='REPORTE DE FACTURAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
#==========FIN DE LOS PDF FSCTURA===============

class ExportarfacturasExcel(DjangoView):
    """
    VISTA PARA EXPORTAR FACTURAS A EXCEL
    Obtiene todas las facturas y las exporta en formato Excel
    """
    
    def get(self, request):
        # Obtener todas las facturas
        facturas = Factura.objects.all()
        
        # Definir las columnas que se mostraran en el reporte
        columnas = ['ID', 'Venta', 'Total', 'Método de pago', 'Fecha']
        
        # Preparar los datos en  tuplas
        datos = [
            (factura.id, factura.venta, factura.valor_total, factura.metodo_pago, factura.fecha_hora)
            for factura in facturas
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Facturas_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE FACTURAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )

