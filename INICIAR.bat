@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
title Antigravity - NucleoTallerV1
color 0A

echo.
echo   ======================================
echo     ANTIGRAVITY - Sistema de Ordenes
echo   ======================================
echo.

cd /d "%~dp0"

REM Crear carpeta de logs
if not exist "logs" mkdir logs

REM Archivo de log con fecha
set LOGFILE=logs\startup.log
echo [%date% %time%] === INICIO DE ARRANQUE === >> "%LOGFILE%"

REM ================================================
REM  Verificar si el servidor ya esta corriendo
REM ================================================
echo   [..] Verificando si el sistema ya esta activo...

powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/NucleoTallerV1/login' -UseBasicParsing -TimeoutSec 2; exit 0 } catch { exit 1 }" >nul 2>&1

if !errorlevel! equ 0 (
    echo   [OK] El sistema ya esta en ejecucion.
    echo   [OK] Abriendo sesion de Login...
    echo.
    echo [%date% %time%] Sistema ya activo. Abriendo nuevo Login. >> "%LOGFILE%"
    start "" http://127.0.0.1:8000/NucleoTallerV1/login
    timeout /t 3 >nul
    exit /b 0
)

echo   [--] Sistema no detectado. Iniciando...
echo [%date% %time%] Sistema no activo. Procediendo con arranque. >> "%LOGFILE%"

REM ================================================
REM  Verificar entorno virtual
REM ================================================
if not exist ".venv\Scripts\activate.bat" (
    echo   [ERROR] No se encontro el entorno virtual .venv
    echo   [ERROR] Ejecute primero: python setup_local.py
    echo.
    echo [%date% %time%] ERROR: Entorno virtual .venv no encontrado. >> "%LOGFILE%"
    echo [%date% %time%] Solucion: Ejecutar python setup_local.py >> "%LOGFILE%"
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
echo   [OK] Entorno virtual activado
echo [%date% %time%] Entorno virtual activado. >> "%LOGFILE%"

REM ================================================
REM  Verificar dependencias
REM ================================================
python -c "import uvicorn" 2>nul
if !errorlevel! neq 0 (
    echo   [!] Faltan dependencias. Instalando...
    echo [%date% %time%] Dependencias faltantes. Instalando... >> "%LOGFILE%"
    pip install -r requirements.txt >> "%LOGFILE%" 2>&1
    if !errorlevel! neq 0 (
        echo   [ERROR] Fallo la instalacion de dependencias.
        echo [%date% %time%] ERROR: pip install fallo. >> "%LOGFILE%"
        pause
        exit /b 1
    )
)
echo   [OK] Dependencias verificadas

REM ================================================
REM  Verificar conexion a PostgreSQL
REM ================================================
echo   [..] Verificando conexion a PostgreSQL...
python -c "from app.database import engine; c=engine.connect(); c.close(); print('OK')" >nul 2>> "%LOGFILE%"
if !errorlevel! neq 0 (
    echo   [ERROR] No se pudo conectar a PostgreSQL.
    echo   [ERROR] Verifique que el servicio PostgreSQL este activo.
    echo.
    echo [%date% %time%] ERROR: Conexion a PostgreSQL fallida. >> "%LOGFILE%"
    echo [%date% %time%] Verifique: servicio PostgreSQL activo, credenciales en app/database.py >> "%LOGFILE%"
    pause
    exit /b 1
)
echo   [OK] PostgreSQL conectado

echo [%date% %time%] Todas las verificaciones pasaron. >> "%LOGFILE%"
echo.
echo   ----------------------------------------
echo     Sistema listo. Abriendo navegador...
echo     http://127.0.0.1:8000/NucleoTallerV1/login
echo   ----------------------------------------
echo.
echo     Presione Ctrl+C para detener
echo   ----------------------------------------
echo.

REM ================================================
REM  Abrir navegador en LOGIN y arrancar servidor
REM ================================================
echo [%date% %time%] Iniciando Uvicorn en puerto 8000... >> "%LOGFILE%"

REM Esperar 2 seg y abrir navegador en /login
start /b cmd /c "timeout /t 2 /nobreak >nul & start "" http://127.0.0.1:8000/NucleoTallerV1/login"

REM Iniciar servidor (errores al log)
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 2>> "%LOGFILE%"

REM Si llega aqui, el servidor se detuvo
echo.
echo   [!] Servidor detenido.
echo [%date% %time%] Servidor detenido. >> "%LOGFILE%"
pause
