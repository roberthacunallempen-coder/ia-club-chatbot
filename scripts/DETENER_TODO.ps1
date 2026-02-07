#!/usr/bin/env pwsh
# DETENER_TODO.ps1
# Script para detener Backend + Frontend

Write-Host "=====================================" -ForegroundColor Red
Write-Host "   DETENIENDO SISTEMA" -ForegroundColor Red
Write-Host "=====================================" -ForegroundColor Red
Write-Host ""

# Detener procesos que usan los puertos
Write-Host "Buscando procesos..." -ForegroundColor Yellow

# Detener Backend (puerto 8000)
$backendProcess = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
if ($backendProcess) {
    Write-Host "  Deteniendo Backend (PID: $backendProcess)..." -ForegroundColor Yellow
    Stop-Process -Id $backendProcess -Force -ErrorAction SilentlyContinue
    Write-Host "  ✓ Backend detenido" -ForegroundColor Green
} else {
    Write-Host "  ℹ Backend no está corriendo" -ForegroundColor Gray
}

# Detener Frontend (puerto 5173)
$frontendProcess = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
if ($frontendProcess) {
    Write-Host "  Deteniendo Frontend (PID: $frontendProcess)..." -ForegroundColor Yellow
    Stop-Process -Id $frontendProcess -Force -ErrorAction SilentlyContinue
    Write-Host "  ✓ Frontend detenido" -ForegroundColor Green
} else {
    Write-Host "  ℹ Frontend no está corriendo" -ForegroundColor Gray
}

Write-Host ""
Write-Host "✓ Sistema detenido completamente" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona cualquier tecla para cerrar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
