from django.shortcuts import render
from django.views.generic import View
from django.views import View as DjangoView
from django.http import HttpResponse
from app.models import *
from app.utils import exportar_pdf, exportar_excel
from datetime import datetime

# ====== VISTAS PARA EXPORTAR REPORTES INSUMOS======

class ExportarinsumosPDF(DjangoView):
    """
    VISTA PARA EXPORTAR INSUMOS A PDF
    Obtiene todos los insumos y los exporta en formato PDF
    """    
    def get(self, request):
        # Obtener todos los insumos
        insumos = insumo.objects.all()
        
        # Definir las columnas que se muestran en el reporte
        columnas = ['id_insumo', 'nombre', 'descripcion', 'categoria', 'stock', 'valor']       
        # Preparar los datos en formato de tuplas
        datos = [
            (i.id_insumo, i.nombre, i.descripcion, i.categoria, i.stock, i.valor)
            for i in insumos
        ]      
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Insumos_{datetime.now().strftime("%d_%m_%Y")}'
        # Llamar funcion de exportacion a PDF
        return exportar_pdf(
            titulo='REPORTE DE INSUMOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )

class ExportarinsumosExcel(DjangoView):
    """
    VISTA PARA EXPORTAR INSUMOS A EXCEL
    Obtiene todos los insumos y los exporta en formato Excel
    """   
    def get(self, request):
        # Obtener todos los insumos
        insumos = insumo.objects.all()       
        # Definir las columnas que se mostraran en el reporte
        columnas = ['id_insumo', 'nombre', 'descripcion', 'categoria', 'stock', 'valor']
        # Preparar los datos en  tuplas
        datos = [
            (insumo.id_insumo, str(insumo.nombre), str(insumo.descripcion), str(insumo.categoria), insumo.stock, insumo.valor)
            for insumo in insumos
        ]      
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Insumos_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE INSUMOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
    