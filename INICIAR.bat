@echo off
setlocal enabledelayedexpansion
REM ======================================================
REM ANTIGRAVITY - Sistema de Ordenes (NucleoTallerV1)
REM ======================================================

REM Forzar codificacion UTF-8 para la consola
chcp 65001 >nul 2>&1

title Antigravity - NucleoTallerV1
color 0A

echo.
echo   ======================================
echo     ANTIGRAVITY - Sistema de Ordenes
echo   ======================================
echo.

REM Asegurar que estamos en la carpeta del script
cd /d "%~dp0"

REM Crear carpeta de logs si no existe
if not exist "logs" mkdir logs
set LOGFILE=logs\startup.log
echo [%date% %time%] === INICIO DE ARRANQUE === >> "%LOGFILE%"

REM ================================================
REM  Seleccion de Version
REM ================================================
echo.
echo   [1] Iniciar Version PYTHON (FastAPI) - Puerto 8000
echo   [2] Iniciar Version PHP (LAMP) - Puerto 8085
echo.
set /p OPTION="Elija la version a iniciar (1/2): "

if "%OPTION%"=="2" goto START_PHP

echo   [..] Verificando si el sistema Python ya esta activo...

powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/NucleoTallerV1/login' -UseBasicParsing -TimeoutSec 2; exit 0 } catch { exit 1 }" >nul 2>&1

if !errorlevel! equ 0 (
    echo   [OK] El sistema Python ya esta en ejecucion en el puerto 8000.
    echo   [OK] Abriendo sesion de Login...
    echo.
    echo [%date% %time%] Sistema Python ya activo. Abriendo nuevo Login. >> "%LOGFILE%"
    start "" http://127.0.0.1:8000/NucleoTallerV1/login
    timeout /t 3 >nul
    exit /b 0
)

echo   [--] Sistema Python no detectado. Iniciando proceso de arranque...
echo [%date% %time%] Sistema Python no activo. Procediendo con arranque. >> "%LOGFILE%"

REM ================================================
REM  Verificar entorno virtual (.venv)
REM ================================================
REM Verificamos la ruta absoluta para evitar ambiguedades
set VENV_PATH=%~dp0.venv
if not exist "%VENV_PATH%\Scripts\activate.bat" (
    echo   [ERROR] No se encontro el entorno virtual en: %VENV_PATH%
    echo   [TIP]   Ejecute primero: python setup_local.py
    echo.
    echo [%date% %time%] ERROR: .venv no encontrado en %VENV_PATH% >> "%LOGFILE%"
    pause
    exit /b 1
)

call "%VENV_PATH%\Scripts\activate.bat"
echo   [OK] Entorno virtual activado.
echo [%date% %time%] Entorno virtual activado. >> "%LOGFILE%"

REM ================================================
REM  Verificar dependencias criticas
REM ================================================
python -c "import uvicorn, fastapi, sqlalchemy, psycopg2" 2>nul
if !errorlevel! neq 0 (
    echo   [!] Faltan dependencias criticas en el entorno. Instalando...
    echo [%date% %time%] Dependencias faltantes. Instalando desde requirements.txt... >> "%LOGFILE%"
    pip install -r requirements.txt >> "%LOGFILE%" 2>&1
    if !errorlevel! neq 0 (
        echo   [ERROR] No se pudieron instalar las dependencias automaticamente.
        echo   [TIP]   Ejecute 'pip install -r requirements.txt' manualmente.
        echo [%date% %time%] ERROR: pip install fallo. >> "%LOGFILE%"
        pause
        exit /b 1
    )
)
echo   [OK] Dependencias verificadas.

REM ================================================
REM  Verificar / Arrancar PostgreSQL
REM ================================================
echo   [..] Verificando conexion a PostgreSQL...
python -c "from app.database import engine; c=engine.connect(); c.close(); print('OK')" >nul 2>nul
if !errorlevel! neq 0 (
    echo   [!] Base de Datos no responde. Intentando levantar servicio...
    echo [%date% %time%] DB no responde. Probando 'net start'... >> "%LOGFILE%"
    
    REM Intentar nombres comunes de servicio de Postgres
    net start postgresql-x64-16 >nul 2>&1
    if !errorlevel! neq 0 net start postgresql-x64-15 >nul 2>&1
    if !errorlevel! neq 0 net start postgresql-x64-14 >nul 2>&1
    if !errorlevel! neq 0 net start postgresql >nul 2>&1
    
    REM Esperar a que el servicio estabilice
    timeout /t 4 /nobreak >nul
    
    python -c "from app.database import engine; c=engine.connect(); c.close(); print('OK')" >nul 2>nul
    if !errorlevel! neq 0 (
        echo   [ERROR] No se pudo levantar PostgreSQL automaticamente.
        echo   [TIP]   Asegurese de abrir este script como ADMINISTRADOR.
        echo   [TIP]   O inicie el servicio manualmente desde 'Services.msc'.
        echo [%date% %time%] ERROR: No se pudo conectar a PostgreSQL tras intento de arranque. >> "%LOGFILE%"
        pause
        exit /b 1
    )
    echo   [OK] PostgreSQL arrancado exitosamente.
)
echo   [OK] Conexion a Base de Datos establecida.

REM ================================================
REM  Lanzamiento Final
REM ================================================
echo.
echo   ----------------------------------------
echo     SISTEMA LISTO. Levantando Aliso Web...
echo     URL: http://127.0.0.1:8000/NucleoTallerV1/login
echo   ----------------------------------------
echo.
echo [%date% %time%] Iniciando Uvicorn... >> "%LOGFILE%"

REM Abrir navegador con retraso para que el servidor este listo
start /b cmd /c "timeout /t 3 /nobreak >nul & start "" http://127.0.0.1:8000/NucleoTallerV1/login"

REM Arrancar servidor Python
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --log-level info

echo.
echo   [!] Servidor Python detenido.
echo [%date% %time%] Servidor Python detenido. >> "%LOGFILE%"
pause
exit /b 0

:START_PHP
echo.
echo   ----------------------------------------
echo     SISTEMA LISTO. Levantando Version PHP (LAMP)...
echo     URL: http://127.0.0.1:8080/NucleoTallerPHP/public/
echo   ----------------------------------------
echo.
echo [%date% %time%] Iniciando Servidor Embebido PHP... >> "%LOGFILE%"

REM Asumimos que php está en el PATH o en la carpeta local php_bin
set PHP_EXE=php
if exist "%~dp0php_bin\php.exe" set PHP_EXE="%~dp0php_bin\php.exe"

%PHP_EXE% -v >nul 2>&1
if !errorlevel! neq 0 (
    echo   [ERROR] PHP no se encuentra en el PATH ni en la carpeta local.
    pause
    exit /b 1
)

start /b cmd /c "timeout /t 2 /nobreak >nul & start "" http://127.0.0.1:8085/NucleoTallerPHP/public/"

%PHP_EXE% -S 127.0.0.1:8085 -t NucleoTallerPHP/public

echo.
echo   [!] Servidor PHP detenido.
echo [%date% %time%] Servidor PHP detenido. >> "%LOGFILE%"
pause
exit /b 0
