@echo off
:: INICIAR_TODO.bat
:: Script simple para iniciar todo el sistema

echo =====================================
echo    INICIANDO SISTEMA COMPLETO
echo =====================================
echo.

:: Ejecutar el script PowerShell
powershell.exe -ExecutionPolicy Bypass -File "%~dp0INICIAR_TODO.ps1"

pause
