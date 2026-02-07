#!/usr/bin/env pwsh
# INICIAR_TODO.ps1
# Script para iniciar Backend + Frontend automáticamente

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "   INICIANDO SISTEMA COMPLETO" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Obtener la ruta del script
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendPath = Join-Path $scriptPath "backend"
$frontendPath = Join-Path $scriptPath "frontend"

# Función para verificar si un puerto está en uso
function Test-Port {
    param([int]$Port)
    $connection = Test-NetConnection -ComputerName localhost -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue
    return $connection
}

# Verificar puertos
Write-Host "[1/4] Verificando puertos..." -ForegroundColor Yellow

$backendRunning = Test-Port -Port 8000
$frontendRunning = Test-Port -Port 5173

if ($backendRunning) {
    Write-Host "  ⚠️  Puerto 8000 (Backend) ya está en uso" -ForegroundColor Yellow
    Write-Host "  El backend probablemente ya está corriendo" -ForegroundColor Gray
} else {
    Write-Host "  ✓ Puerto 8000 disponible" -ForegroundColor Green
}

if ($frontendRunning) {
    Write-Host "  ⚠️  Puerto 5173 (Frontend) ya está en uso" -ForegroundColor Yellow
    Write-Host "  El frontend probablemente ya está corriendo" -ForegroundColor Gray
} else {
    Write-Host "  ✓ Puerto 5173 disponible" -ForegroundColor Green
}

Write-Host ""

# Iniciar Backend
if (-not $backendRunning) {
    Write-Host "[2/4] Iniciando Backend..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; Write-Host 'BACKEND INICIADO' -ForegroundColor Green; python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"
    Write-Host "  ✓ Backend iniciando en http://localhost:8000" -ForegroundColor Green
    Start-Sleep -Seconds 3
} else {
    Write-Host "[2/4] Backend ya está corriendo" -ForegroundColor Gray
}

Write-Host ""

# Iniciar Frontend
if (-not $frontendRunning) {
    Write-Host "[3/4] Iniciando Frontend..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; Write-Host 'FRONTEND INICIADO' -ForegroundColor Green; npm run dev"
    Write-Host "  ✓ Frontend iniciando en http://localhost:5173" -ForegroundColor Green
    Start-Sleep -Seconds 2
} else {
    Write-Host "[3/4] Frontend ya está corriendo" -ForegroundColor Gray
}

Write-Host ""
Write-Host "[4/4] Sistema listo!" -ForegroundColor Green
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "   ACCESOS:" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "  Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "  Test Bot: http://localhost:5173/test-bot" -ForegroundColor White
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona cualquier tecla para cerrar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
