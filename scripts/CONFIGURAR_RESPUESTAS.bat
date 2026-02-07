@echo off
:: Script para configurar la longitud de las respuestas del bot

cd /d "%~dp0backend"

echo =====================================
echo   CONFIGURAR LONGITUD DE RESPUESTAS
echo =====================================
echo.

python configurar_longitud_respuestas.py

echo.
pause
