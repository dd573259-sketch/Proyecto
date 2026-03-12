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
    
class ExportarCategoriasPDF(DjangoView):
    def get(self, request):
        categorias = Categoria.objects.all()
        columnas = ['ID', 'Nombre', 'Descripción','Estado', 'Fecha_creacion']
        datos = [( cat.id , cat.nombre , cat.descripcion, cat.estado, cat.fecha_creacion) for cat in categorias]
        
        nombre_archivo = f'Reporte_Categorias_{datetime.now().strftime("%d_%m_%Y")}'
        
        return exportar_pdf(
            titulo='REPORTE DE CATEGORIAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
class ExportarCategoriasExcel(DjangoView):
    """
    VISTA PARA EXPORTAR CATEGORIAS A EXCEL
    Obtiene todas las categorias y las exporta en formato Excel
    """
    
    def get(self, request):
        # Obtener todas las categorias 
        categorias = Categoria.objects.all()
        
        # Definir las columnas que se mostraran en el reporte
        columnas = ['ID', 'Nombre', 'Descripcion', 'Estado']
        
        # Preparar los datos en  tuplas
        datos = [
            (cat.id, cat.nombre, cat.descripcion, cat.estado)
            for cat in categorias
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Categorias_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE CATEGORIAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
