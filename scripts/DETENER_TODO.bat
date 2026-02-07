@echo off
:: DETENER_TODO.bat
:: Script para detener todo el sistema

echo =====================================
echo    DETENIENDO SISTEMA
echo =====================================
echo.

powershell.exe -ExecutionPolicy Bypass -File "%~dp0DETENER_TODO.ps1"

pause
