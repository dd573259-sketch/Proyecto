"""
VISTAS PARA RESPALDO Y RESTAURACION DE BD 
Permite crear respaldo completo y restaurarlo desde archivo SQL
"""
import os
import subprocess
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings

# ========== OBTENER DATOS DE LA BD ==========
def obtener_credenciales_mysql():
    """Obtiene las credenciales de MySQL desde settings.py"""
    db_config = settings.DATABASES['default']
    return {
        'host': db_config.get('HOST', 'localhost'),
        'user': db_config.get('USER', 'root'),
        'password': db_config.get('PASSWORD', ' '),
        'database': db_config.get('NAME', 'la_tuna'),
        'port': db_config.get('PORT', 3306),
        'mysql_path': r'C:\Program Files\MySQL\MySQL Server 8.0\bin',
    }

def probar_conexion_mysql():
    """Prueba la conexión a MySQL"""
    creds = obtener_credenciales_mysql()
    try:
        cmd = [
            os.path.join(creds["mysql_path"], 'mysql.exe'),
            '-h', creds["host"],
            '-u', creds["user"],
            '-P', str(creds["port"]),
            '--password=' + creds["password"],
            '-e', 'SELECT 1;',
            creds["database"]
        ]

        resultado = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )

        return resultado.returncode == 0
    except:
        return False

# ========== VISTA PARA MOSTRAR OPCIONES DE RESPALDO ==========
@require_http_methods(["GET", "POST"])
def backup(request):
    """Muestra el menu de opciones para respaldo y restauracion"""
    if request.method == "POST":
        accion = request.POST.get('accion')

        try:
            if accion == 'backup_completo':
                # Verificar conexion antes de hacer respaldo
                if not probar_conexion_mysql():
                    return JsonResponse({'error': 'No se puede conectar a MySQL. Verifica que el servidor este en ejecucion y el user y pass  sean validos.'}, status=400)
                return realizar_respaldo_completo()
    
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    # Verificar conexion para mostrar estado
    mysql_ok = probar_conexion_mysql()
    context = {
        'titulo': 'Respaldo y Restauracion de Base de Datos',
        'mysql_conectado': mysql_ok,
    }
    return render(request, 'backup/menu.html', context)

# ========== VISTA PARA RESTAURAR DATOS ==========
@require_http_methods(["POST"])
def restaurar_datos(request):
    """Restaura datos desde un archivo SQL"""
    if 'archivo' not in request.FILES:
        return JsonResponse({'error': 'No se proporciono archivo'}, status=400)

    archivo = request.FILES['archivo']

    try:
        # Validar que sea .sql
        if not archivo.name.endswith('.sql'):
            return JsonResponse({'error': 'El archivo debe tener extension .sql'}, status=400)

        # Leer contenido del archivo
        contenido_sql = archivo.read().decode('utf-8')

        # Restaurar la BD desde el SQL
        restaurar_bd_desde_sql(contenido_sql)

        mensaje = " Base de datos restaurada correctamente"
        return JsonResponse({'exito': True, 'mensaje': mensaje})

    except Exception as e:
        return JsonResponse({'error': f'Error al restaurar: {str(e)}'}, status=400)

# ========== FUNCIONES DE RESPALDO ==========

def realizar_respaldo_completo():
    """Realiza un respaldo completo (estructura + datos)"""
    creds = obtener_credenciales_mysql()

    try:
        cmd = [
            os.path.join(creds["mysql_path"], 'mysqldump.exe'),
            '-h', creds["host"],
            '-u', creds["user"],
            '-P', str(creds["port"]),
            f'--password={creds["password"]}',
            '--routines',
            '--triggers',
            '--events',
            creds["database"]
        ]

        resultado = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=60
        )

        if resultado.returncode != 0:
            raise Exception(f"Error mysqldump: {resultado.stderr}")

        sql_content = resultado.stdout

        if not sql_content or not sql_content.strip():
            raise Exception("El respaldo está vacío")

        sql_content = (
            f"-- Respaldo Completo de {creds['database']}\n"
            f"-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"-- Tipo: Completo (Estructura + Datos)\n\n"
            + sql_content
        )

        return generar_archivo_descarga(sql_content, 'backup_completo')

    except subprocess.TimeoutExpired:
        raise Exception("Timeout al ejecutar mysqldump")

    except Exception as e:
        print(f"Error en respaldo completo: {str(e)}")
        raise Exception(f"Error en respaldo completo: {str(e)}")

# ========== FUNCIONES PARA RESTAURAR ==========

def restaurar_bd_desde_sql(contenido_sql):
    """Restaura la BD ejecutando el SQL"""
    creds = obtener_credenciales_mysql()

    try:
        # Construir comando mysql usando la misma ruta donde estan los binarios
        cmd = [
            os.path.join(creds["mysql_path"], 'mysql.exe'),
            '-h', creds["host"],
            '-u', creds["user"],
            '-P', str(creds["port"]),
            '--password=' + creds["password"],
            creds["database"]
        ]

        # Ejecutar el CLI de mysql para importar el contenido
        proceso = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = proceso.communicate(input=contenido_sql, timeout=120)  


        if proceso.returncode != 0:
            raise Exception(f"Error MySQL: {stderr}")

        return True

    except subprocess.TimeoutExpired:
        raise Exception("Timeout al restaurar la base de datos")
    except Exception as e:
        print(f"Error al restaurar: {str(e)}")
        raise Exception(f"Error al restaurar: {str(e)}")

# ========== FUNCION PARA GENERAR DESCARGA ==========

def generar_archivo_descarga(contenido_sql, nombre_archivo):
    """Genera un archivo SQL para descargar"""
    response = HttpResponse(contenido_sql.encode('utf-8'), content_type='application/sql')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}_{timestamp}.sql"'

    return response


def backup_ventas(request):
    """Exporta solo los datos de la tabla venta"""

# ========== PEDIDOS ==========

def backup_pedidos(request):
    """Exporta solo los datos de la tabla pedido"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    if not probar_conexion_mysql():
        return JsonResponse({'error': 'No se puede conectar a MySQL'}, status=400)
    
    try:
        creds = obtener_credenciales_mysql()
        cmd = [
            os.path.join(creds["mysql_path"], 'mysqldump.exe'),
            '-h', creds["host"],
            '-u', creds["user"],
            '-P', str(creds["port"]),
            '--password=' + creds["password"],
            creds["database"],
            'pedido'  # solo esta tabla
        ]
        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if resultado.returncode != 0:
            raise Exception(f"Error mysqldump: {resultado.stderr}")
        
        sql_content = f"-- Backup Pedidos\n-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n" + resultado.stdout
        return generar_archivo_descarga(sql_content, 'backup_pedidos')
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ========== CLIENTES ==========

def backup_clientes(request):
    """Exporta solo los datos de la tabla cliente"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    if not probar_conexion_mysql():
        return JsonResponse({'error': 'No se puede conectar a MySQL'}, status=400)
    
    try:
        creds = obtener_credenciales_mysql()
        cmd = [
            os.path.join(creds["mysql_path"], 'mysqldump.exe'),
            '-h', creds["host"],
            '-u', creds["user"],
            '-P', str(creds["port"]),
            '--password=' + creds["password"],
            creds["database"],
            'cliente'  # solo esta tabla
        ]
        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if resultado.returncode != 0:
            raise Exception(f"Error mysqldump: {resultado.stderr}")
        
        sql_content = f"-- Backup Clientes\n-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n" + resultado.stdout
        return generar_archivo_descarga(sql_content, 'backup_clientes')
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
        
# ========== USUARIOS  ==========

def backup_usuarios(request):
    """Exporta solo los datos de la tabla usuario"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    if not probar_conexion_mysql():
        return JsonResponse({'error': 'No se puede conectar a MySQL'}, status=400)
    
    try:
        creds = obtener_credenciales_mysql()
        cmd = [
            os.path.join(creds["mysql_path"], 'mysqldump.exe'),
            '-h', creds["host"],
            '-u', creds["user"],
            '-P', str(creds["port"]),
            '--password=' + creds["password"],
            creds["database"],
            'usuario'  # solo esta tabla
        ]
        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if resultado.returncode != 0:
            raise Exception(f"Error mysqldump: {resultado.stderr}")
        
        sql_content = f"-- Backup usuarios\n-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n" + resultado.stdout
        return generar_archivo_descarga(sql_content, 'backup_usuarios')
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def backup_pagos(request):
    """Exporta solo los datos de la tabla pago"""
# ========== PROVEEDORES  ==========

def backup_proveedores(request):
    """Exporta solo los datos de la tabla proveedor"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    if not probar_conexion_mysql():
        return JsonResponse({'error': 'No se puede conectar a MySQL'}, status=400)
    
    try:
        creds = obtener_credenciales_mysql()
        cmd = [
            os.path.join(creds["mysql_path"], 'mysqldump.exe'),
            '-h', creds["host"],
            '-u', creds["user"],
            '-P', str(creds["port"]),
            '--password=' + creds["password"],
            creds["database"],
            'proveedor'  # solo esta tabla
        ]
        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if resultado.returncode != 0:
            raise Exception(f"Error mysqldump: {resultado.stderr}")
        
        sql_content = f"-- Backup Proveedores\n-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n" + resultado.stdout
        return generar_archivo_descarga(sql_content, 'backup_proveedores')
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def backup_facturas(request):
    """Exporta solo los datos de la tabla factura"""
    
# ========== PRODUCTOS  ==========

def backup_productos(request):
    """Exporta solo los datos de la tabla producto"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    if not probar_conexion_mysql():
        return JsonResponse({'error': 'No se puede conectar a MySQL'}, status=400)
    
    try:
        creds = obtener_credenciales_mysql()
        cmd = [
            os.path.join(creds["mysql_path"], 'mysqldump.exe'),
            '-h', creds["host"],
            '-u', creds["user"],
            '-P', str(creds["port"]),
            '--password=' + creds["password"],
            creds["database"],
            'producto'  # solo esta tabla
        ]
        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if resultado.returncode != 0:
            raise Exception(f"Error mysqldump: {resultado.stderr}")
        
        sql_content = f"-- Backup Productos\n-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n" + resultado.stdout
        return generar_archivo_descarga(sql_content, 'backup_productos')
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# RESPALDO PACHECO
def backup_insumos(request):
    """Exporta solo los datos de la tabla insumo"""

    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    if not probar_conexion_mysql():
        return JsonResponse({'error': 'No se puede conectar a MySQL'}, status=400)
    
    try:
        creds = obtener_credenciales_mysql()
        cmd = [
            os.path.join(creds["mysql_path"], 'mysqldump.exe'),
            '-h', creds["host"],
            '-u', creds["user"],
            '-P', str(creds["port"]),
            '--password=' + creds["password"],
            creds["database"],
            'venta'  # solo esta tabla
        ]
        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if resultado.returncode != 0:
            raise Exception(f"Error mysqldump: {resultado.stderr}")
        
        sql_content = f"-- Backup Insumos\n-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n" + resultado.stdout
        return generar_archivo_descarga(sql_content, 'backup_insumos')
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
# ========== COMPRAS ==========

def backup_compras(request):
    """Exporta solo los datos de la tabla compra"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    if not probar_conexion_mysql():
        return JsonResponse({'error': 'No se puede conectar a MySQL'}, status=400)
    
    try:
        creds = obtener_credenciales_mysql()
        cmd = [
            os.path.join(creds["mysql_path"], 'mysqldump.exe'),
            '-h', creds["host"],
            '-u', creds["user"],
            '-P', str(creds["port"]),
            '--password=' + creds["password"],
            creds["database"],
            'compra'  # solo esta tabla
        ]
        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if resultado.returncode != 0:
            raise Exception(f"Error mysqldump: {resultado.stderr}")
        
        sql_content = f"-- Backup Compras\n-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n" + resultado.stdout
        return generar_archivo_descarga(sql_content, 'backup_compras')
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def backup_facturas(request):
    """Exporta solo los datos de la tabla factura"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    if not probar_conexion_mysql():
        return JsonResponse({'error': 'No se puede conectar a MySQL'}, status=400)
    
    try:
        creds = obtener_credenciales_mysql()
        cmd = [
            os.path.join(creds["mysql_path"], 'mysqldump.exe'),
            '-h', creds["host"],
            '-u', creds["user"],
            '-P', str(creds["port"]),
            '--password=' + creds["password"],
            creds["database"],
            'factura'  # solo esta tabla
        ]
        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if resultado.returncode != 0:
            raise Exception(f"Error mysqldump: {resultado.stderr}")
        
        sql_content = f"-- Backup Facturas\n-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n" + resultado.stdout
        return generar_archivo_descarga(sql_content, 'backup_facturas')
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
