@echo off
title Liberar Puerto 8000
color 0C

echo ========================================
echo      LIBERAR PUERTO 8000
echo ========================================
echo.
echo Este script detendra cualquier proceso
echo que este usando el puerto 8000
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0LIBERAR_PUERTO_8000.ps1"
