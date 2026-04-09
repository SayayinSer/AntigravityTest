@echo off
chcp 65001 >nul 2>&1
title Antigravity - Work Order Management
color 0A

echo.
echo   ======================================
echo     ANTIGRAVITY - Sistema de Ordenes
echo   ======================================
echo.

cd /d "%~dp0"

:: Verificar si existe el entorno virtual
if not exist ".venv\Scripts\activate.bat" (
    echo   [!] No se encontro el entorno virtual.
    echo   [!] Ejecute primero: python setup_local.py
    echo.
    pause
    exit /b 1
)

:: Activar entorno virtual
call .venv\Scripts\activate.bat

:: Verificar si uvicorn esta instalado
python -c "import uvicorn" 2>nul
if errorlevel 1 (
    echo   [!] Faltan dependencias. Instalando...
    pip install -r requirements.txt
)

echo   [OK] Entorno listo
echo   [>>] Iniciando servidor...
echo.
echo   ----------------------------------------
echo     Abra su navegador en:
echo     http://127.0.0.1:8000
echo   ----------------------------------------
echo     Usuario: SU
echo     Clave:   123456
echo   ----------------------------------------
echo.
echo     Presione Ctrl+C para detener
echo   ----------------------------------------
echo.

:: Abrir navegador automaticamente
start "" http://127.0.0.1:8000

:: Iniciar el servidor
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

pause
