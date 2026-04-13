@echo off
:: Cambiar a la unidad y carpeta del proyecto
C:
cd "C:\workspace\La tuna\Proyecto\Proyecto_GP4"

:: Forzar página de códigos UTF-8
chcp 65001 > nul

:: Crear carpeta de logs si no existe
if not exist "logs" mkdir logs

:: Escribir inicio de ejecución en el log
echo ======================================== >> logs\vencimiento.log
echo %date% %time% - INICIANDO EJECUCION >> logs\vencimiento.log
echo ======================================== >> logs\vencimiento.log

:: Ejecutar el comando de Django
"C:\workspace\La tuna\Proyecto\Proyecto_GP4\.venv\Scripts\python.exe" manage.py verificar_vencimientos >> logs\vencimiento.log 2>&1

:: Escribir fin de ejecución
echo %date% %time% - EJECUCION FINALIZADA >> logs\vencimiento.log
echo. >> logs\vencimiento.log