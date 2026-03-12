from django.shortcuts import render
from django.views.generic import View
from django.views import View as DjangoView
from django.http import HttpResponse
from app.models import *
from app.utils import exportar_pdf, exportar_excel
from datetime import datetime

# ====== VISTAS PARA EXPORTAR REPORTES proveedores ======

class ExportarProveedoresPDF(DjangoView):
    """
    VISTA PARA EXPORTAR PROVEEDORES A PDF
    Obtiene todos los proveedores y los exporta en formato PDF
    """

    
    def get(self, request):
        # Obtener todas las categorias 
        proveedor = Proveedor.objects.all()
        
        # Definir las columnas que se muestran en el reporte
        columnas = ['ID', 'Nombre', 'Telefono', 'Correo', 'Direccion']
        
        # Preparar los datos en formato de tuplas
        datos = [
            (cat.id_proveedor, cat.nombre_proveedor, cat.telefono, cat.correo_electronico, cat.direccion)
            for cat in proveedor
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Proveedores_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a PDF
        return exportar_pdf(
            titulo='REPORTE DE PROVEEDORES',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )


class ExportarProveedoresExcel(DjangoView):
    """
    VISTA PARA EXPORTAR PROVEEDORES A EXCEL
    Obtiene todos los proveedores y los exporta en formato Excel
    """
    
    def get(self, request):
        # Obtener todas las categorias 
        proveedor = Proveedor.objects.all()
        
        # Definir las columnas que se mostraran en el reporte
        columnas = ['ID', 'Nombre', 'Telefono', 'Correo', 'Direccion']
        
        # Preparar los datos en  tuplas
        datos = [
            (cat.id_proveedor, cat.nombre_proveedor, cat.telefono, cat.correo_electronico, cat.direccion)
            for cat in proveedor
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Proveedores_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE PROVEEDORES',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
    

# ====== VISTAS PARA EXPORTAR REPORTES productos ======

class ExportarProductosPDF(DjangoView):
    """
    VISTA PARA EXPORTAR PRODUCTOS A PDF
    Obtiene todos los productos y los exporta en formato PDF
    """

    
    def get(self, request):
        # Obtener todas las categorias 
        producto = Producto.objects.all()
        
        # Definir las columnas que se muestran en el reporte
        columnas = ['ID', 'Nombre', 'Unidad', 'Precio', 'Stock', 'Fecha de Ingreso', 'Fecha de Vencimiento']
        
        # Preparar los datos en formato de tuplas
        datos = [
            (cat.id_producto, cat.nombre, cat.unidad, cat.precio, cat.stock, cat.fecha_ingreso, cat.fecha_vencimiento)
            for cat in producto
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Productos_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a PDF
        return exportar_pdf(
            titulo='REPORTE DE PRODUCTOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )


class ExportarProductosExcel(DjangoView):
    """
    VISTA PARA EXPORTAR PRODUCTOS A EXCEL
    Obtiene todos los productos y los exporta en formato Excel
    """
    
    def get(self, request):
        # Obtener todas las categorias 
        producto = Producto.objects.all()
        
        # Definir las columnas que se mostraran en el reporte
        columnas = ['ID', 'NOMBRE', 'UNIDAD', 'PRECIO', 'STOCK', 'FECHA DE NGRESO', 'FECHA DE VENCIMIENTO']
        
        # Preparar los datos en  tuplas
        datos = [
            (cat.id_producto, cat.nombre, cat.unidad, cat.precio, cat.stock, cat.fecha_ingreso, cat.fecha_vencimiento)
            for cat in producto
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Productos_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE PRODUCTOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )


# ====== VISTAS PARA EXPORTAR REPORTES compras ======

class ExportarcomprasPDF(DjangoView):
    """
    VISTA PARA EXPORTAR COMPRAS A PDF
    Obtiene todas las compras y las exporta en formato PDF
    """

    
    def get(self, request):
        # Obtener todas las categorias 
        compra = Compra.objects.all()
        
        # Definir las columnas que se muestran en el reporte
        columnas = ['ID', 'PROVEEDOR','PRODUCTO', 'INSUMO', 'FECHA COMPRA', 'ESTADO PAGO', 'TOTAL']
        
        # Preparar los datos en formato de tuplas
        datos = [
            (cat.id_compra, cat.proveedor, cat.producto, cat.insumo, cat.fecha_compra, cat.estado_pago, cat.total_compra)
            for cat in compra
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Compras_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a PDF
        return exportar_pdf(
            titulo='REPORTE DE COMPRAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )


class ExportarcomprasExcel(DjangoView):
    """
    VISTA PARA EXPORTAR COMPRAS A EXCEL
    Obtiene todas las compras y las exporta en formato Excel
    """
    
    def get(self, request):
        # Obtener todas las categorias 
        compra = Compra.objects.all()
        
        # Definir las columnas que se mostraran en el reporte
        columnas = ['ID', 'PROVEEDOR', 'PRODUCTO', 'INSUMO', 'FECHA COMPRA', 'ESTADO PAGO', 'TOTAL']
        
        # Preparar los datos en  tuplas
        datos = [
            (cat.id_compra,str(cat.proveedor), str(cat.producto), str(cat.insumo), cat.fecha_compra.replace(tzinfo=None), cat.estado_pago, cat.total_compra)
            for cat in compra
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Compras_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE COMPRAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
    