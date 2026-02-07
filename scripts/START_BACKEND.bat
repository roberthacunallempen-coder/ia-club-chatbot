@echo off
title IA Club - Backend Server
color 0A

echo ========================================
echo      IA CLUB - BACKEND SERVER
echo ========================================
echo.
echo Iniciando servidor backend...
echo.

REM Ejecutar el script de PowerShell simplificado
powershell -ExecutionPolicy Bypass -File "%~dp0START_BACKEND_ONLY.ps1"

echo.
echo Servidor detenido.
echo Presiona cualquier tecla para salir...
pause > nul
