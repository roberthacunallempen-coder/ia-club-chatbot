@echo off
title IA Club Chatbot - Iniciando Sistema
color 0A

echo ========================================
echo      IA CLUB CHATBOT SYSTEM
echo ========================================
echo.
echo Opciones de inicio:
echo.
echo 1. Iniciar SOLO el backend (recomendado para desarrollo)
echo 2. Iniciar backend + ngrok (para integracion con Chatwoot)
echo.
set /p opcion="Selecciona una opcion (1 o 2): "

if "%opcion%"=="1" (
    echo.
    echo Iniciando solo el backend...
    powershell -ExecutionPolicy Bypass -File "%~dp0START_BACKEND_ONLY.ps1"
) else if "%opcion%"=="2" (
    echo.
    echo Iniciando backend + ngrok...
    powershell -ExecutionPolicy Bypass -File "%~dp0START_BOT.ps1"
) else (
    echo.
    echo Opcion invalida. Iniciando solo el backend...
    timeout /t 2 > nul
    powershell -ExecutionPolicy Bypass -File "%~dp0START_BACKEND_ONLY.ps1"
)

echo.
echo Presiona cualquier tecla para cerrar esta ventana...
pause > nul
