@echo off
title IA Club Chatbot - Deteniendo Servidores
color 0C

echo ========================================
echo      DETENER SERVIDORES IA CLUB
echo ========================================
echo.
echo Deteniendo todos los servidores...
echo.

REM Ejecutar el script de PowerShell mejorado
powershell -ExecutionPolicy Bypass -File "%~dp0STOP_BOT.ps1"

pause
