# ========================================
# SCRIPT DE DETENCIÓN DEL BOT IA CLUB
# ========================================

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  DETENIENDO BOT IA CLUB + CHATWOOT  " -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Detener procesos Python del backend
Write-Host "Deteniendo backend..." -ForegroundColor Yellow
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*BOT PYTHON*" }
if ($pythonProcesses) {
    $pythonProcesses | Stop-Process -Force
    Write-Host "✓ Backend detenido ($($pythonProcesses.Count) procesos)" -ForegroundColor Green
} else {
    Write-Host "  No hay procesos del backend corriendo" -ForegroundColor Gray
}

# Detener ngrok
Write-Host "Deteniendo ngrok..." -ForegroundColor Yellow
$ngrokProcesses = Get-Process ngrok -ErrorAction SilentlyContinue
if ($ngrokProcesses) {
    $ngrokProcesses | Stop-Process -Force
    Write-Host "✓ ngrok detenido ($($ngrokProcesses.Count) procesos)" -ForegroundColor Green
} else {
    Write-Host "  No hay procesos de ngrok corriendo" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "  SISTEMA DETENIDO                   " -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
