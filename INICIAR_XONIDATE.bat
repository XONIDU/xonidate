@echo off
title XONIDATE 2026 - Generador Automático de Citas
color 0A

:: ============================================================
:: SOLICITAR PERMISOS DE ADMINISTRADOR
:: ============================================================
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Solicitando permisos de administrador...
    echo.
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B
)

:: ============================================================
:: EJECUTAR start.py CON PERMISOS DE ADMINISTRADOR
:: ============================================================
cls
echo ============================================================
echo           XONIDATE 2026 - Generador Automatico de Citas
echo              (Modo Administrador)
echo ============================================================
echo.
echo [OK] Permisos de administrador obtenidos
echo.
echo Iniciando XONIDATE...
echo.
echo [INFO] Generador de citas aleatorias con PDF
echo [INFO] Accede a: http://localhost:5000
echo.
echo [INFO] Caracteristicas:
echo   - Gestion de asistentes
echo   - Dias disponibles
echo   - Comidas y lugares
echo   - Generacion de PDF elegante
echo.
echo Presiona Ctrl+C para detener el servidor
echo ============================================================
echo.

python start.py

pause
