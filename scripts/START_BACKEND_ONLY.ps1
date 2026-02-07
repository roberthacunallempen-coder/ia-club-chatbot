# ========================================
# INICIO SIMPLE DEL BACKEND (SIN NGROK)
# ========================================

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  INICIANDO BOT IA CLUB - BACKEND   " -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "Directorio de trabajo: $scriptDir" -ForegroundColor Gray
Write-Host ""

# 1. Verificar entorno virtual
Write-Host "[1/2] Verificando Python..." -ForegroundColor Yellow

if (Test-Path "$scriptDir\backend\venv\Scripts\python.exe") {
    Write-Host "   Usando entorno virtual" -ForegroundColor Green
    $pythonExe = "$scriptDir\backend\venv\Scripts\python.exe"
} else {
    Write-Host "   Usando Python del sistema" -ForegroundColor Yellow
    $pythonExe = "python"
}

# Verificar version de Python
try {
    $pythonVersion = & $pythonExe --version
    Write-Host "   $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ERROR: Python no encontrado" -ForegroundColor Red
    Write-Host "   Instala Python o crea el entorno virtual" -ForegroundColor Red
    Write-Host ""
    Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# 2. Verificar archivo .env
Write-Host ""
Write-Host "[2/2] Verificando configuracion..." -ForegroundColor Yellow

if (Test-Path "$scriptDir\backend\.env.local") {
    Write-Host "   Archivo .env.local encontrado" -ForegroundColor Green
} else {
    Write-Host "   ADVERTENCIA: No se encuentra .env.local" -ForegroundColor Yellow
    Write-Host "   El backend usara configuracion por defecto" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "     INICIANDO SERVIDOR BACKEND     " -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "El servidor se iniciara en http://localhost:8000" -ForegroundColor Cyan
Write-Host "(Si el puerto esta ocupado, se te daran opciones)" -ForegroundColor Gray
Write-Host ""
Write-Host "URLs de acceso:" -ForegroundColor Cyan
Write-Host "  Backend API:      http://localhost:8000" -ForegroundColor White
Write-Host "  Documentacion:    http://localhost:8000/docs" -ForegroundColor White
Write-Host "  Health Check:     http://localhost:8000/health" -ForegroundColor White
Write-Host ""
Write-Host "Endpoints disponibles:" -ForegroundColor Cyan
Write-Host "  /knowledge         - Gestion de conocimientos" -ForegroundColor White
Write-Host "  /faqs              - Gestion de FAQs" -ForegroundColor White
Write-Host "  /templates         - Plantillas de mensajes (NUEVO)" -ForegroundColor Green
Write-Host "  /flows             - Flujos conversacionales" -ForegroundColor White
Write-Host "  /webhook/chatwoot  - Webhook de Chatwoot" -ForegroundColor White
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio backend
Set-Location "$scriptDir\backend"

# Verificar si el puerto 8000 está en uso
Write-Host "Verificando puerto 8000..." -ForegroundColor Gray
$portInUse = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

if ($portInUse) {
    Write-Host ""
    Write-Host "ADVERTENCIA: El puerto 8000 ya está en uso" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Opciones:" -ForegroundColor Cyan
    Write-Host "  1. Matar el proceso y continuar" -ForegroundColor White
    Write-Host "  2. Usar puerto 8001 en su lugar" -ForegroundColor White
    Write-Host "  3. Cancelar" -ForegroundColor White
    Write-Host ""
    $opcion = Read-Host "Selecciona una opcion (1, 2 o 3)"
    
    if ($opcion -eq "1") {
        Write-Host "Deteniendo proceso en puerto 8000..." -ForegroundColor Yellow
        $process = Get-Process -Id $portInUse.OwningProcess -ErrorAction SilentlyContinue
        if ($process) {
            Stop-Process -Id $process.Id -Force
            Write-Host "Proceso detenido" -ForegroundColor Green
            Start-Sleep -Seconds 2
        }
        $port = 8000
    } elseif ($opcion -eq "2") {
        Write-Host "Usando puerto 8001" -ForegroundColor Green
        $port = 8001
    } else {
        Write-Host "Cancelado" -ForegroundColor Red
        exit 0
    }
} else {
    $port = 8000
}

Write-Host ""
Write-Host "Iniciando servidor en puerto $port..." -ForegroundColor Green
Write-Host ""

# Iniciar el servidor
& $pythonExe -m uvicorn app.main:app --host 0.0.0.0 --port $port --reload
